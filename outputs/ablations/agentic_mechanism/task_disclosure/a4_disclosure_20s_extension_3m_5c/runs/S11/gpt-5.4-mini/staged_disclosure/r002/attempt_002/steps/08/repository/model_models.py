from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping, Sequence


def _to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "model_dump"):
        dumped = value.model_dump()
        if isinstance(dumped, Mapping):
            return dict(dumped)
    if hasattr(value, "dict"):
        dumped = value.dict()
        if isinstance(dumped, Mapping):
            return dict(dumped)
    raise TypeError(f"Expected mapping-like value, got {type(value)!r}")


def _normalize_messages(messages: Sequence[Any] | None) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for message in messages or []:
        item = _to_dict(message)
        role = str(item.get("role", "user")).strip() or "user"
        content = item.get("content", "")
        if content is None:
            content = ""
        normalized.append({"role": role, "content": str(content), **{k: v for k, v in item.items() if k not in {"role", "content"}}})
    return normalized


def _normalize_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(metadata or {})


@dataclass(slots=True)
class ManagedModelRequest:
    model: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_input(cls, data: Any) -> "ManagedModelRequest":
        payload = _to_dict(data)
        return cls(
            model=str(payload.get("model", "")).strip(),
            messages=_normalize_messages(payload.get("messages")),
            temperature=payload.get("temperature"),
            max_tokens=payload.get("max_tokens"),
            top_p=payload.get("top_p"),
            metadata=_normalize_metadata(payload.get("metadata")),
        )

    def normalized(self) -> dict[str, Any]:
        result: dict[str, Any] = {"model": self.model, "messages": _normalize_messages(self.messages)}
        if self.temperature is not None:
            result["temperature"] = float(self.temperature)
        if self.max_tokens is not None:
            result["max_tokens"] = int(self.max_tokens)
        if self.top_p is not None:
            result["top_p"] = float(self.top_p)
        if self.metadata:
            result["metadata"] = _normalize_metadata(self.metadata)
        return result


@dataclass(slots=True)
class ManagedModelChoice:
    index: int = 0
    message: dict[str, Any] = field(default_factory=dict)
    finish_reason: str | None = None

    @classmethod
    def from_input(cls, data: Any) -> "ManagedModelChoice":
        payload = _to_dict(data)
        return cls(
            index=int(payload.get("index", 0)),
            message=_to_dict(payload.get("message")),
            finish_reason=payload.get("finish_reason"),
        )

    def normalized(self) -> dict[str, Any]:
        result: dict[str, Any] = {"index": int(self.index), "message": _to_dict(self.message)}
        if self.finish_reason is not None:
            result["finish_reason"] = str(self.finish_reason)
        return result


@dataclass(slots=True)
class ManagedModelResponse:
    id: str
    model: str
    choices: list[ManagedModelChoice] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_input(cls, data: Any) -> "ManagedModelResponse":
        payload = _to_dict(data)
        choices = [ManagedModelChoice.from_input(choice) for choice in payload.get("choices", []) or []]
        return cls(
            id=str(payload.get("id", "")).strip(),
            model=str(payload.get("model", "")).strip(),
            choices=choices,
            usage=_normalize_metadata(payload.get("usage")),
            metadata=_normalize_metadata(payload.get("metadata")),
        )

    def normalized(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "model": self.model,
            "choices": [choice.normalized() for choice in self.choices],
        }
        if self.usage:
            result["usage"] = _normalize_metadata(self.usage)
        if self.metadata:
            result["metadata"] = _normalize_metadata(self.metadata)
        return result
