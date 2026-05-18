from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class PulseProfile(BaseModel):
    """Base model for all extracted digital identities."""
    platform: str
    username: str
    data: Dict[str, Any]

class BasePlatform(ABC):
    """Abstract base class for all platform extractors."""
    
    @abstractmethod
    def __init__(self, auth_config: Dict[str, str]):
        pass

    @abstractmethod
    async def extract(self) -> PulseProfile:
        """Core extraction logic for the platform."""
        pass

    @abstractmethod
    def to_markdown(self, profile: PulseProfile) -> str:
        """Converts the extracted profile into LLM-friendly Markdown."""
        pass
