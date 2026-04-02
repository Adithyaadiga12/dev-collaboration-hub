from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ── What user sends when CREATING ──────────────────────
class ProjectCreate(BaseModel):
    title: str                           # required
    description: Optional[str] = None   # optional
    github_url: Optional[str] = None    # optional
    is_open: Optional[bool] = True      # optional, defaults True

# ── What user sends when UPDATING ──────────────────────
class ProjectUpdate(BaseModel):
    title: Optional[str] = None          # all optional
    description: Optional[str] = None   # send only what you want to change
    github_url: Optional[str] = None
    is_open: Optional[bool] = None

# ── What server sends BACK ──────────────────────────────
class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    github_url: Optional[str]
    is_open: bool
    owner_id: int                        # who created it
    created_at: datetime                 # when it was created

    class Config:
        from_attributes = True