from fastapi import FastAPI, HTTPException, Query
import os
import httpx
import asyncio

app = FastAPI()

# Base URL for GitHub API.
GITHUB_API_URL = "https://api.github.com"

# Retrieve GitHub token from environment variables.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN environment variable must be set.")

# Set headers for GitHub API requests.
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ----------------------------
# Repository Operations
# ----------------------------

@app.post("/repositories/")
async def create_repository(name: str, description: str = "", private: bool = False):
    """
    Creates a new GitHub repository.
    """
    url = f"{GITHUB_API_URL}/user/repos"
    payload = {
        "name": name,
        "description": description,
        "private": private,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.delete("/repositories/{owner}/{repo}")
async def delete_repository(owner: str, repo: str):
    """
    Deletes the specified GitHub repository.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=HEADERS)
    if response.status_code == 204:
        return {"message": "Repository deleted successfully."}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.get("/repositories/")
async def list_repositories():
    """
    Lists GitHub repositories for the authenticated user.
    """
    url = f"{GITHUB_API_URL}/user/repos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

# ----------------------------
# Pull Request Operations
# ----------------------------

@app.get("/repositories/{owner}/{repo}/pull_requests")
async def list_pull_requests(
    owner: str,
    repo: str,
    limit: int = Query(10, description="Maximum number of pull requests to return")
):
    """
    Retrieves open pull requests for the given repository along with contributors (the GitHub user who created the pull request).
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": "open", "per_page": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        pulls = response.json()
        result = []
        for pull in pulls:
            pr_number = pull.get("number")
            contributor = pull.get("user", {}).get("login")
            result.append({"pull_number": pr_number, "contributor": contributor})
        return {"pull_requests": result}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

# ----------------------------
# Simulated CI/CD Pipeline
# ----------------------------

async def run_tests():
    # Simulate an asynchronous task for running tests.
    await asyncio.sleep(2)
    return "Tests passed."

async def run_lint():
    # Simulate an asynchronous task for linting.
    await asyncio.sleep(1)
    return "Lint passed."

async def run_security():
    # Simulate an asynchronous security check.
    await asyncio.sleep(1)
    return "Security check passed."

async def run_deployment():
    # Simulate a deployment step.
    await asyncio.sleep(3)
    return "Deployment successful."

@app.post("/pipeline/")
async def run_pipeline():
    """
    Runs a simulated CI/CD pipeline performing tests, lint, security checks, and deployment.
    """
    results = {}
    results["tests"] = await run_tests()
    results["lint"] = await run_lint()
    results["security"] = await run_security()
    results["deployment"] = await run_deployment()

    return results
