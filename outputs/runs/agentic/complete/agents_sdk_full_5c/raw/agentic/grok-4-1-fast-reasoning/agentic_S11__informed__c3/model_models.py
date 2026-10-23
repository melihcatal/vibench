from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class PlatformInvokeRequest:
    model: Optional[str]
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    stream: bool = False

@dataclass
class PlatformResponse:
    content: str
    metadata: Optional[Dict[str, Any]] = None