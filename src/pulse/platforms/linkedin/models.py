from typing import List
from pydantic import BaseModel

class Post(BaseModel):
    content: str

class LinkedInData(BaseModel):
    profile_id: str
    posts: List[Post] = []
