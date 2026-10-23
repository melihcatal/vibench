from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ModelRequest:
    prompt: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelResponse:
    text: str
    provider: str
    model: str
    raw: Any = None


@dataclass
class NormalizedPlatformOutput:
    text: str
    provider: str
    model: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())
