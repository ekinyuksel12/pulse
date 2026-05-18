import random
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from pulse.core.base import BasePlatform, PulseProfile
from .models import LinkedInData, Post

class LinkedInPlatform(BasePlatform):
    """
    Pulse implementation for LinkedIn data extraction.
    Designed for reliability and stealth-focused archival.
    """
    
    def __init__(self, auth_config: Dict[str, str]):
        self.li_at = auth_config.get("li_at")
        self.profile_id = auth_config.get("profile_id")
        self.session = requests.Session()
        self.session.cookies.set("li_at", self.li_at)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        })

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=20),
        retry=retry_if_exception_type(requests.exceptions.RequestException),
        reraise=True
    )
    def _fetch_page(self, url: str) -> str:
        time.sleep(random.uniform(2, 5))
        resp = self.session.get(url, timeout=20)
        
        if resp.status_code == 999:
            logger.error("LinkedIn Blocked (999). Backing off.")
            raise requests.exceptions.RequestException("LinkedIn Blocked (999)")
            
        resp.raise_for_status()
        return resp.text

    async def extract(self) -> PulseProfile:
        """Extracts LinkedIn activity data."""
        logger.info(f"👣 Pulse: Scraping LinkedIn footprint for {self.profile_id}")
        url = f"https://www.linkedin.com/in/{self.profile_id}/recent-activity/shares/"
        
        try:
            html = self._fetch_page(url)
            soup = BeautifulSoup(html, "html.parser")
            
            posts = []
            for sec in soup.find_all(['div', 'section']):
                txt = sec.get_text(strip=True)
                if 100 < len(txt) < 5000 and "log in" not in txt.lower():
                    posts.append(Post(content=txt[:2000]))
            
            data = LinkedInData(profile_id=self.profile_id, posts=posts)
            
            return PulseProfile(
                platform="linkedin",
                username=self.profile_id,
                data=data.model_dump()
            )
        except Exception as e:
            logger.error(f"LinkedIn extraction failed: {e}")
            raise

    def to_markdown(self, profile: PulseProfile) -> str:
        data = LinkedInData(**profile.data)
        md = f"# LinkedIn Data: {profile.username}\n\n"
        md += "## Activity & Posts\n\n"
        for post in data.posts:
            md += f"- {post.content}\n\n----- \n\n"
        
        md += "---\n*Extracted with Pulse*\n"
        return md
