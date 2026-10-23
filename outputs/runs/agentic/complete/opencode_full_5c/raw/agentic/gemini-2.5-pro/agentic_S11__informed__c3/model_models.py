from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class PlatformRequest:
    model_name: str
    prompt: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResponse:
    text: str
    provider_response: Optional[Any] = None


@dataclass
class PlatformResponseWithMetadata(PlatformResponse):
    usage_metadata: Optional[Dict[str, Any]] = None
    model_id: Optional[str] = None
