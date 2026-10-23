from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class PlatformModelPayload:
    text: str


@dataclass
class PlatformModelOutput:
    text: str
    metadata: Optional[Dict[str, Any]] = None
