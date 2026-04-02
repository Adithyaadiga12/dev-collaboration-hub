from pydantic import BaseModel
from typing import Optional

class GitHubRepoResponse(BaseModel):
    name: str
    description: Optional[str]
    stars: int
    forks: int
    language: Optional[str]
    last_updated: str
    url : str

