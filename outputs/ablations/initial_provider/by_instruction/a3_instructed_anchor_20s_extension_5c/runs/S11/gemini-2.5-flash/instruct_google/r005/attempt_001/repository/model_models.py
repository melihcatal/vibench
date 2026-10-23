from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class PlatformModelRequest:
    prompt: str
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class PlatformModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None
    safety_attributes: Optional[Dict[str, Any]] = None
