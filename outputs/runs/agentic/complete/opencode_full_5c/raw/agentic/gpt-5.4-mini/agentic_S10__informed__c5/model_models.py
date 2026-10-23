from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MessageSpec:
    role: str
    content: str


@dataclass
class TextRequest:
    prompt: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: Optional[int] = None


@dataclass
class TextResponse:
    text: str
    model: str
    raw: Any = None


def normalize_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    return [
        {"role": m.get("role", "user"), "content": str(m.get("content", ""))}
        for m in messages
    ]


def to_dict(obj):
    return asdict(obj) if hasattr(obj, "__dataclass_fields__") else obj
