import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.schemas.github import GitHubRepoResponse
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/projects",
    tags=["GitHub"]
)

@router.get("/{project_id}/github", response_model=GitHubRepoResponse)
def get_github_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Step 1: Find the project
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Step 2: Does this project have a GitHub URL?
    if not project.github_url:
        raise HTTPException(
            status_code=400,
            detail="This project has no GitHub URL linked"
        )

    # Step 3: Extract owner and repo name from URL
    # "https://github.com/adithya/my-app" → ["adithya", "my-app"]
    try:
        parts = project.github_url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]
    except IndexError:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub URL format"
        )

    # Step 4: Call GitHub's API
    github_api_url = f"https://api.github.com/repos/{owner}/{repo}"

    with httpx.Client(follow_redirects=True) as client:
        response = client.get(
        github_api_url,
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    print(f"GitHub Status: {response.status_code}")   # ← add this
    print(f"GitHub URL called: {github_api_url}") 

    # Step 5: Did GitHub respond successfully?
    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="GitHub repository not found — check the URL"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch data from GitHub"
        )

    # Step 6: Parse the response
    data = response.json()

    # Step 7: Return only the fields we care about
    return GitHubRepoResponse(
        name=data["name"],
        description=data.get("description"),
        stars=data["stargazers_count"],
        forks=data["forks_count"],
        language=data.get("language"),
        last_updated=data["updated_at"],
        url=data["html_url"]
    )