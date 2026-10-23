from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


@dataclass(frozen=True)
class PlatformMessage:
    role: str
    content: str
    name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"role": self.role, "content": self.content}
        if self.name is not None:
            data["name"] = self.name
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data


@dataclass(frozen=True)
class PlatformRequest:
    messages: Sequence[PlatformMessage]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"messages": [m.to_dict() for m in self.messages]}
        if self.model is not None:
            data["model"] = self.model
        if self.temperature is not None:
            data["temperature"] = self.temperature
        if self.max_tokens is not None:
            data["max_tokens"] = self.max_tokens
        if self.top_p is not None:
            data["top_p"] = self.top_p
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data


@dataclass(frozen=True)
class PlatformUsage:
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.input_tokens is not None:
            data["input_tokens"] = self.input_tokens
        if self.output_tokens is not None:
            data["output_tokens"] = self.output_tokens
        if self.total_tokens is not None:
            data["total_tokens"] = self.total_tokens
        if self.extra:
            data.update(self.extra)
        return data


@dataclass(frozen=True)
class PlatformResponse:
    output: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Optional[PlatformUsage] = None
    raw: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"output": self.output}
        if self.model is not None:
            data["model"] = self.model
        if self.resource_id is not None:
            data["resource_id"] = self.resource_id
        if self.usage is not None:
            data["usage"] = self.usage.to_dict()
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        if self.raw is not None:
            data["raw"] = self.raw
        return data


def _coerce_usage(value: Any) -> Optional[PlatformUsage]:
    if value is None:
        return None
    if isinstance(value, PlatformUsage):
        return value
    if isinstance(value, Mapping):
        known = {k: value.get(k) for k in ("input_tokens", "output_tokens", "total_tokens")}
        extra = {k: v for k, v in value.items() if k not in known}
        return PlatformUsage(
            input_tokens=known["input_tokens"],
            output_tokens=known["output_tokens"],
            total_tokens=known["total_tokens"],
            extra=dict(extra),
        )
    return None


def _extract_text(output: Any) -> str:
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, Mapping):
        for key in ("output", "text", "content", "message"):
            value = output.get(key)
            if isinstance(value, str):
                return value
        choices = output.get("choices")
        if isinstance(choices, Sequence) and choices:
            first = choices[0]
            if isinstance(first, Mapping):
                message = first.get("message")
                if isinstance(message, Mapping):
                    content = message.get("content")
                    if isinstance(content, str):
                        return content
                text = first.get("text")
                if isinstance(text, str):
                    return text
    return str(output)


def normalize_platform_response(value: Any) -> PlatformResponse:
    if isinstance(value, PlatformResponse):
        return value
    if isinstance(value, Mapping):
        output = _extract_text(value)
        usage = _coerce_usage(value.get("usage"))
        model = value.get("model") if isinstance(value.get("model"), str) else None
        resource_id = None
        for key in ("resource_id", "id", "handle", "deployment_id", "inference_profile_id"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                resource_id = candidate
                break
        metadata = {k: v for k, v in value.items() if k not in {"output", "text", "content", "message", "choices", "usage", "model", "resource_id", "id", "handle", "deployment_id", "inference_profile_id"}}
        return PlatformResponse(output=output, model=model, resource_id=resource_id, usage=usage, raw=value, metadata=metadata)
    return PlatformResponse(output=_extract_text(value), raw=value)


def normalize_platform_request(value: Any) -> PlatformRequest:
    if isinstance(value, PlatformRequest):
        return value
    if isinstance(value, Mapping):
        messages: List[PlatformMessage] = []
        raw_messages = value.get("messages")
        if isinstance(raw_messages, Iterable):
            for item in raw_messages:
                if isinstance(item, PlatformMessage):
                    messages.append(item)
                elif isinstance(item, Mapping):
                    messages.append(
                        PlatformMessage(
                            role=str(item.get("role", "user")),
                            content=str(item.get("content", "")),
                            name=item.get("name") if isinstance(item.get("name"), str) else None,
                            metadata={k: v for k, v in item.items() if k not in {"role", "content", "name"}},
                        )
                    )
        return PlatformRequest(
            messages=messages,
            model=value.get("model") if isinstance(value.get("model"), str) else None,
            temperature=value.get("temperature") if isinstance(value.get("temperature"), (int, float)) else None,
            max_tokens=value.get("max_tokens") if isinstance(value.get("max_tokens"), int) else None,
            top_p=value.get("top_p") if isinstance(value.get("top_p"), (int, float)) else None,
            metadata={k: v for k, v in value.items() if k not in {"messages", "model", "temperature", "max_tokens", "top_p"}},
        )
    return PlatformRequest(messages=[PlatformMessage(role="user", content=str(value))])


def build_platform_request(
    messages: Sequence[Union[PlatformMessage, Mapping[str, Any], str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    metadata: Optional[Mapping[str, Any]] = None,
) -> PlatformRequest:
    normalized: List[PlatformMessage] = []
    for item in messages:
        if isinstance(item, PlatformMessage):
            normalized.append(item)
        elif isinstance(item, Mapping):
            normalized.append(
                PlatformMessage(
                    role=str(item.get("role", "user")),
                    content=str(item.get("content", "")),
                    name=item.get("name") if isinstance(item.get("name"), str) else None,
                    metadata={k: v for k, v in item.items() if k not in {"role", "content", "name"}},
                )
            )
        else:
            normalized.append(PlatformMessage(role="user", content=str(item)))
    return PlatformRequest(
        messages=normalized,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        metadata=dict(metadata or {}),
    )
