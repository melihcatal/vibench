from dataclasses import dataclass
from typing import Any


@dataclass
class PlatformPrompt:
    text: str


@dataclass
class PlatformResult:
    text: str
    resource_id: str | None = None
    model: str | None = None
    usage: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def extract_message_text(response: Any) -> str:
    choices = getattr(response, "choices", None) or []
    if not choices:
        return ""
    message = getattr(choices[0], "message", None)
    if message is None:
        return ""
    content = getattr(message, "content", None)
    return normalize_text(content)


def response_metadata(response: Any) -> dict[str, Any]:
    return {
        "id": getattr(response, "id", None),
        "model": getattr(response, "model", None),
        "created": getattr(response, "created", None),
        "system_fingerprint": getattr(response, "system_fingerprint", None),
    }
