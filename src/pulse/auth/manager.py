import os
import json
from typing import Dict, Optional
from pathlib import Path

class AuthManager:
    """Manages credentials for various platforms."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path(os.getenv("PULSE_HOME", Path.home() / ".pulse"))
        self.auth_file = self.config_dir / "auth.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if not self.auth_file.exists():
            with open(self.auth_file, 'w') as f:
                json.dump({}, f)

    def get_auth(self, platform: str) -> Dict[str, str]:
        """Retrieves auth configuration for a platform."""
        with open(self.auth_file, 'r') as f:
            data = json.load(f)
        return data.get(platform, {})

    def save_auth(self, platform: str, config: Dict[str, str]):
        """Saves auth configuration for a platform."""
        with open(self.auth_file, 'r') as f:
            data = json.load(f)
        
        data[platform] = config
        
        with open(self.auth_file, 'w') as f:
            json.dump(data, f, indent=4)

    def clear_auth(self, platform: str):
        """Removes auth for a specific platform."""
        with open(self.auth_file, 'r') as f:
            data = json.load(f)
        
        if platform in data:
            del data[platform]
            with open(self.auth_file, 'w') as f:
                json.dump(data, f, indent=4)
