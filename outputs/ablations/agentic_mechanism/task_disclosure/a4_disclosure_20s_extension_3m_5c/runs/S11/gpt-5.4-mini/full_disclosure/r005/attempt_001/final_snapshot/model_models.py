from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union


@dataclass(frozen=True)
class PlatformRequest:
    model: str
    input: Union[str, Sequence[str], Sequence[Mapping[str, Any]], Mapping[str, Any]]
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlatformUsage:
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlatformResource:
    provider: str
    resource_id: Optional[str] = None
    model_handle: Optional[str] = None
    deployment_id: Optional[str] = None
    inference_profile_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlatformResponse:
    output: str
    model: Optional[str] = None
    locale: Optional[str] = None
    usage: Optional[PlatformUsage] = None
    resource: Optional[PlatformResource] = None
    raw: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedPlatformOutput:
    text: str
    locale: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[PlatformUsage] = None
    resource: Optional[PlatformResource] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("output", "text", "content", "message", "response"):
            if key in value and value[key] is not None:
                return normalize_text_output(value[key])
        return ""
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        parts: List[str] = []
        for item in value:
            normalized = normalize_text_output(item)
            if normalized:
                parts.append(normalized)
        return "".join(parts)
    return str(value)


def normalize_usage(value: Any) -> Optional[PlatformUsage]:
    if value is None:
        return None
    if isinstance(value, PlatformUsage):
        return value
    if not isinstance(value, Mapping):
        return None
    known = {k: value.get(k) for k in ("input_tokens", "output_tokens", "total_tokens")}
    extra = {k: v for k, v in value.items() if k not in known}
    return PlatformUsage(
        input_tokens=known["input_tokens"],
        output_tokens=known["output_tokens"],
        total_tokens=known["total_tokens"],
        extra=extra,
    )


def normalize_resource(value: Any) -> Optional[PlatformResource]:
    if value is None:
        return None
    if isinstance(value, PlatformResource):
        return value
    if not isinstance(value, Mapping):
        return None
    known = {k: value.get(k) for k in ("provider", "resource_id", "model_handle", "deployment_id", "inference_profile_id")}
    extra = {k: v for k, v in value.items() if k not in known}
    return PlatformResource(
        provider=str(known["provider"] or ""),
        resource_id=known["resource_id"],
        model_handle=known["model_handle"],
        deployment_id=known["deployment_id"],
        inference_profile_id=known["inference_profile_id"],
        extra=extra,
    )


def normalize_platform_response(value: Any) -> PlatformResponse:
    if isinstance(value, PlatformResponse):
        return value
    if isinstance(value, Mapping):
        output = normalize_text_output(value.get("output", value.get("text", value.get("content", value))))
        usage = normalize_usage(value.get("usage"))
        resource = normalize_resource(value.get("resource") or value.get("platform_resource") or value.get("model_resource"))
        metadata = {k: v for k, v in value.items() if k not in {"output", "text", "content", "usage", "resource", "platform_resource", "model_resource"}}
        return PlatformResponse(
            output=output,
            model=value.get("model"),
            locale=value.get("locale"),
            usage=usage,
            resource=resource,
            raw=value,
            metadata=metadata,
        )
    return PlatformResponse(output=normalize_text_output(value), raw=value)


def normalize_platform_output(value: Any) -> NormalizedPlatformOutput:
    response = normalize_platform_response(value)
    return NormalizedPlatformOutput(
        text=response.output,
        locale=response.locale,
        model=response.model,
        usage=response.usage,
        resource=response.resource,
        metadata=dict(response.metadata),
    )
