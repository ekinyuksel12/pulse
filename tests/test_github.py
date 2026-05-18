import pytest
import httpx
from unittest.mock import MagicMock, patch
from pulse.platforms.github.processor import GitHubPlatform
from pulse.core.base import PulseProfile

@pytest.mark.anyio
@patch('httpx.AsyncClient.get')
async def test_github_extract(mock_get):
    # Mock user profile
    mock_resp_profile = MagicMock()
    mock_resp_profile.status_code = 200
    mock_resp_profile.json.return_value = {
        "name": "Test User",
        "bio": "Bio",
        "location": "Earth",
        "public_repos": 1,
        "followers": 10,
        "following": 5
    }
    
    # Mock repositories
    mock_resp_repos = MagicMock()
    mock_resp_repos.status_code = 200
    mock_resp_repos.json.side_effect = [
        [{"name": "repo1", "full_name": "user/repo1", "private": False, "html_url": "url"}],
        [] # Stop pagination
    ]
    
    # Mock languages
    mock_resp_langs = MagicMock()
    mock_resp_langs.status_code = 200
    mock_resp_langs.json.return_value = {"Python": 100}
    
    # Mock readme
    mock_resp_readme = MagicMock()
    mock_resp_readme.status_code = 404 # No readme
    
    # Provide enough responses for profile, repos, and repo details (langs, readme)
    mock_get.side_effect = [
        mock_resp_profile, 
        mock_resp_repos, 
        mock_resp_repos, # second page (empty)
        mock_resp_langs, 
        mock_resp_readme
    ]
    
    platform = GitHubPlatform({"token": "fake", "username": "user"})
    profile = await platform.extract()
    
    assert isinstance(profile, PulseProfile)
    assert profile.platform == "github"
    assert "repo1" in str(profile.data)
    assert "Python" in str(profile.data)
