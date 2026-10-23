from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model_id: Optional[str] = None
    resource_id: Optional[str] = None
    stream: bool = False
    extra: Optional[Dict[str, Any]] = None


@dataclass
class PlatformResponse:
    text: str
    model_id: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(
                    str(
                        item.get("text")
                        or item.get("content")
                        or item.get("delta")
                        or ""
                    )
                )
            else:
                parts.append(str(item))
        return "".join(parts)
    if isinstance(value, dict):
        return str(
            value.get("text")
            or value.get("content")
            or value.get("output_text")
            or value.get("message", {}).get("content")
            or ""
        )
    return str(value)


def normalize_usage(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    return {}
