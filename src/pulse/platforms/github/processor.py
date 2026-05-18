import base64
import asyncio
import httpx
from typing import Dict, Any, List
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from pulse.core.base import BasePlatform, PulseProfile
from .models import GitHubData, RepositoryInfo, UserProfile

class GitHubPlatform(BasePlatform):
    """Pulse implementation for GitHub data extraction."""
    
    BASE_URL = "https://api.github.com"

    def __init__(self, auth_config: Dict[str, str]):
        self.token = auth_config.get("token")
        self.username = auth_config.get("username")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
        reraise=True
    )
    async def _get(self, endpoint: str) -> Any:
        url = f"{self.BASE_URL}{endpoint}"
        response = await self.client.get(url)
        
        if response.status_code == 403 and "rate limit" in response.text.lower():
            logger.warning("GitHub API Rate limit exceeded. Backing off...")
            raise httpx.HTTPStatusError("Rate limit exceeded", request=response.request, response=response)
            
        response.raise_for_status()
        return response.json()

    async def extract(self) -> PulseProfile:
        """Fetches profile and all repository data asynchronously."""
        try:
            logger.info(f"🛰️ Pulse: Fetching GitHub heartbeat for {self.username}")
            
            # Fetch profile
            p_raw = await self._get(f"/users/{self.username}")
            profile = UserProfile(**p_raw)

            # Fetch repos (Paginated)
            repos_raw = []
            page = 1
            while True:
                data = await self._get(f"/user/repos?page={page}&per_page=100&visibility=all")
                if not data: break
                repos_raw.extend(data)
                page += 1

            # Parallel repo details
            tasks = [self._get_repo_details(r) for r in repos_raw]
            repositories = await asyncio.gather(*tasks)
            
            all_skills = {lang for r in repositories for lang in r.languages.keys()}
            
            gh_data = GitHubData(
                profile=profile,
                repositories=list(repositories),
                inferred_skills=list(all_skills)
            )

            return PulseProfile(
                platform="github",
                username=self.username,
                data=gh_data.model_dump()
            )
        finally:
            await self.client.aclose()

    async def _get_repo_details(self, r_data: Dict) -> RepositoryInfo:
        full_name = r_data['full_name']
        langs, readme = await asyncio.gather(
            self._get(f"/repos/{full_name}/languages"),
            self._get_readme(full_name)
        )
        return RepositoryInfo(
            name=r_data["name"],
            full_name=full_name,
            private=r_data["private"],
            url=r_data["html_url"],
            languages=langs,
            readme_snippet=readme[:2000]
        )

    async def _get_readme(self, full_name: str) -> str:
        try:
            data = await self._get(f"/repos/{full_name}/readme")
            return base64.b64decode(data['content']).decode('utf-8')
        except Exception:
            return "No README found."

    def to_markdown(self, profile: PulseProfile) -> str:
        data = GitHubData(**profile.data)
        md = f"# GitHub Profile: {data.profile.name or profile.username}\n\n"
        md += f"**Bio:** {data.profile.bio or 'N/A'}\n"
        md += f"**Inferred Skills:** {', '.join(data.inferred_skills)}\n\n"
        md += "## Repositories\n\n"
        
        for repo in data.repositories:
            status = "Private" if repo.private else "Public"
            md += f"### {repo.name} ({status})\n"
            md += f"- **URL:** {repo.url}\n"
            md += f"- **Languages:** {', '.join(repo.languages.keys())}\n"
            md += f"- **README Snippet:**\n\n```markdown\n{repo.readme_snippet}\n```\n\n"
        
        md += "---\n*Extracted via [Pulse](https://github.com/ekinyuksel12/pulse)* 🛰️\n"
        return md
