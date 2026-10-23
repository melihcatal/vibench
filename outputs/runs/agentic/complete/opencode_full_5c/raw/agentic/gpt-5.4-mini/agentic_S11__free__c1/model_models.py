from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlatformRequest:
    input_text: str
    model: str = "gpt-5.4-mini"
    temperature: float = 0.2


@dataclass
class PlatformResponse:
    text: str
    model: str | None = None
    resource_id: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "".join(normalize_text(v) for v in value)
    return str(value)
