from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model_id: Optional[str] = None
    deployment_id: Optional[str] = None
    resource_id: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    usage: Optional[Dict[str, Any]] = None
    resource_id: Optional[str] = None
    model_id: Optional[str] = None
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def response_text_from_choice(response: Any) -> str:
    try:
        return normalize_text(response.output_text)
    except Exception:
        pass
    try:
        return normalize_text(response.choices[0].message.content)
    except Exception:
        return normalize_text(response)
