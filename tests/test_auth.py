import json
from pathlib import Path
from pulse.auth.manager import AuthManager

def test_auth_manager_save_load(tmp_path):
    # Setup AuthManager with a temp config dir
    config_dir = tmp_path / ".pulse"
    auth_manager = AuthManager(config_dir=config_dir)
    
    platform = "test_platform"
    config = {"key": "value"}
    
    # Test Save
    auth_manager.save_auth(platform, config)
    assert auth_manager.get_auth(platform) == config
    
    # Test Load from file
    with open(config_dir / "auth.json", 'r') as f:
        data = json.load(f)
    assert data[platform] == config

def test_auth_manager_clear(tmp_path):
    config_dir = tmp_path / ".pulse"
    auth_manager = AuthManager(config_dir=config_dir)
    
    auth_manager.save_auth("p1", {"a": "b"})
    auth_manager.clear_auth("p1")
    assert auth_manager.get_auth("p1") == {}
