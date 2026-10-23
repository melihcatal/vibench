from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class PlatformResponse:
    text: str
    raw: Any = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(
            normalize_text(item) for item in value if item is not None
        ).strip()
    if isinstance(value, dict):
        for key in ("text", "content", "output", "message"):
            if key in value:
                return normalize_text(value[key])
    return str(value).strip()


def extract_metadata(raw: Any) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}
    if hasattr(raw, "usage"):
        usage = getattr(raw, "usage")
        metadata["usage"] = (
            usage.model_dump() if hasattr(usage, "model_dump") else usage
        )
    if hasattr(raw, "id"):
        metadata["resource_id"] = getattr(raw, "id")
    if hasattr(raw, "model"):
        metadata["model_handle"] = getattr(raw, "model")
    return metadata
