import pytest
import requests
from unittest.mock import MagicMock, patch
from pulse.platforms.linkedin.processor import LinkedInPlatform

@pytest.mark.anyio
@patch('requests.Session.get')
async def test_linkedin_extract(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><section>This is a test post that is deliberately made to be longer than one hundred characters to ensure it passes the filtration logic in the LinkedIn platform processor. This is essential for a successful test pass.</section></body></html>"
    mock_get.return_value = mock_response
    
    platform = LinkedInPlatform({"li_at": "cookie", "profile_id": "user"})
    profile = await platform.extract()
    
    assert profile.platform == "linkedin"
    assert len(profile.data['posts']) > 0
    assert "test post" in profile.data['posts'][0]['content']
