from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class PlatformRequest:
    prompt: str
    model_id: str = "command-r"
    temperature: float = 0.7
    max_tokens: int = 1024


@dataclass
class PlatformResponse:
    text: str
    model_id: str
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
