from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


def _to_dict(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, Mapping):
        return dict(value)
    return value


@dataclass(frozen=True)
class PlatformRequest:
    prompt: str
    model: Optional[str] = None
    project: Optional[str] = None
    organization: Optional[str] = None
    timeout: Optional[float] = None
    extra_headers: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PlatformResponse:
    model: str
    output_text: str
    response: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedPlatformOutput:
    text: str
    model: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    resource_id: Optional[str] = None
    platform_metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_platform_response(response: Any, *, model: Optional[str] = None) -> NormalizedPlatformOutput:
    payload = _to_dict(response)
    text = ""
    if isinstance(payload, Mapping):
        text = str(payload.get("output_text") or payload.get("text") or "")
    else:
        text = str(getattr(response, "output_text", "") or getattr(response, "text", "") or "")
    usage: Dict[str, Any] = {}
    if isinstance(payload, Mapping):
        raw_usage = payload.get("usage")
        if isinstance(raw_usage, Mapping):
            usage = dict(raw_usage)
    else:
        raw_usage = getattr(response, "usage", None)
        if raw_usage is not None:
            usage = dict(_to_dict(raw_usage)) if isinstance(_to_dict(raw_usage), Mapping) else {"value": _to_dict(raw_usage)}
    resource_id = None
    if isinstance(payload, Mapping):
        resource_id = payload.get("id") or payload.get("resource_id")
    else:
        resource_id = getattr(response, "id", None) or getattr(response, "resource_id", None)
    platform_metadata: Dict[str, Any] = {"raw_response": payload}
    return NormalizedPlatformOutput(
        text=text,
        model=model,
        usage=usage,
        resource_id=resource_id,
        platform_metadata=platform_metadata,
    )


def build_platform_request(prompt: str, **kwargs: Any) -> PlatformRequest:
    return PlatformRequest(prompt=prompt, **kwargs)


def build_platform_response(model: str, output_text: str, response: Any = None, **metadata: Any) -> PlatformResponse:
    return PlatformResponse(model=model, output_text=output_text, response=response, metadata=dict(metadata))
