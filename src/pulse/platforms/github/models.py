from typing import List, Dict, Optional
from pydantic import BaseModel

class UserProfile(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    public_repos: int
    total_private_repos: Optional[int] = None
    followers: int
    following: int

class RepositoryInfo(BaseModel):
    name: str
    full_name: str
    private: bool
    description: Optional[str] = None
    url: str
    topics: List[str] = []
    languages: Dict[str, int]
    readme_snippet: str

class GitHubData(BaseModel):
    profile: UserProfile
    repositories: List[RepositoryInfo]
    inferred_skills: List[str]
