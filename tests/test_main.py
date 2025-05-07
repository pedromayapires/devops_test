from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from ..main import app

client = TestClient(app)

# Mock GitHub API headers
HEADERS = {
    "Authorization": "token FAKE_TOKEN",
    "Accept": "application/vnd.github.v3+json",
}


# -------------------
# Repository Tests
# -------------------


@patch("httpx.AsyncClient.post")
def test_create_repository(mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json = MagicMock()
    mock_post.return_value.json.return_value = {
        "name": "mock-repo",
        "private": False,
    }

    response = client.post(
        "/repositories/",
        headers=HEADERS,
        json={
            "name": "mock-repo",
            "description": "Test repo",
            "private": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "mock-repo"


@patch("httpx.AsyncClient.delete")
def test_delete_repository(mock_delete):
    mock_delete.return_value.status_code = 204

    response = client.delete("/repositories/test-owner/test-repo")
    assert response.status_code == 200
    assert response.json() == {"message": "Repository deleted successfully."}


@patch("httpx.AsyncClient.get")
def test_list_repositories(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = MagicMock()
    mock_get.return_value.json.return_value = [
        {"name": "repo1"},
        {"name": "repo2"},
    ]

    response = client.get("/repositories/")
    assert response.status_code == 200
    assert response.json() == [{"name": "repo1"}, {"name": "repo2"}]


@patch("httpx.AsyncClient.get")
def test_list_pull_requests(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = MagicMock()
    mock_get.return_value.json.return_value = [
        {"number": 1, "user": {"login": "alice"}},
        {"number": 2, "user": {"login": "bob"}},
    ]

    response = client.get(
        "/repositories/test-owner/test-repo/pull_requests", params={"limit": 2}
    )
    assert response.status_code == 200
    assert response.json() == {
        "pull_requests": [
            {"pull_number": 1, "contributor": "alice"},
            {"pull_number": 2, "contributor": "bob"},
        ]
    }
