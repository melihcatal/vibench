from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformRequest:
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResponse:
    text: str
    resource_id: Optional[str] = None
    model_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


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
        for key in ("text", "content", "output", "generation"):
            if key in value:
                return normalize_text(value[key])
    return str(value).strip()


def response_from_payload(payload: Dict[str, Any]) -> PlatformResponse:
    return PlatformResponse(
        text=normalize_text(
            payload.get("text") or payload.get("output") or payload.get("content")
        ),
        resource_id=payload.get("resource_id")
        or payload.get("model_id")
        or payload.get("id"),
        model_id=payload.get("model_id")
        or payload.get("model")
        or payload.get("resource_id"),
        usage=payload.get("usage"),
        metadata={
            k: v
            for k, v in payload.items()
            if k not in {"text", "output", "content", "usage"}
        },
    )
