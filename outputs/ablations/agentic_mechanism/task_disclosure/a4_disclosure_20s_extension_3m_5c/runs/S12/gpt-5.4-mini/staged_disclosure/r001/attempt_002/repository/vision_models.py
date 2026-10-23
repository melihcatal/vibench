from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


@dataclass(frozen=True)
class StaticImageRequest:
    image: str
    prompt: Optional[str] = None
    detail: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"image": self.image}
        if self.prompt is not None:
            data["prompt"] = self.prompt
        if self.detail is not None:
            data["detail"] = self.detail
        if self.temperature is not None:
            data["temperature"] = self.temperature
        if self.max_tokens is not None:
            data["max_tokens"] = self.max_tokens
        return data


@dataclass(frozen=True)
class VisualUnderstandingRequest:
    image: str
    instructions: Optional[str] = None
    question: Optional[str] = None
    detail: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"image": self.image}
        if self.instructions is not None:
            data["instructions"] = self.instructions
        if self.question is not None:
            data["question"] = self.question
        if self.detail is not None:
            data["detail"] = self.detail
        if self.temperature is not None:
            data["temperature"] = self.temperature
        if self.max_tokens is not None:
            data["max_tokens"] = self.max_tokens
        return data


@dataclass(frozen=True)
class StaticImageResponse:
    text: str
    raw: Mapping[str, Any] = field(default_factory=dict)
    model: Optional[str] = None
    usage: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class VisualUnderstandingResponse:
    text: str
    raw: Mapping[str, Any] = field(default_factory=dict)
    model: Optional[str] = None
    usage: Optional[Mapping[str, Any]] = None
    objects: Optional[List[Mapping[str, Any]]] = None
    labels: Optional[List[str]] = None


VisionRequest = Union[StaticImageRequest, VisualUnderstandingRequest]
VisionResponse = Union[StaticImageResponse, VisualUnderstandingResponse]


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        parts: List[str] = []
        for item in value:
            text = _coerce_text(item)
            if text:
                parts.append(text)
        return "\n".join(parts)
    if isinstance(value, Mapping):
        for key in ("text", "content", "message", "output", "response"):
            if key in value:
                text = _coerce_text(value[key])
                if text:
                    return text
        return ""
    return str(value)


def normalize_static_image_response(payload: Mapping[str, Any]) -> StaticImageResponse:
    text = _coerce_text(
        payload.get("text")
        or payload.get("output")
        or payload.get("content")
        or payload.get("result")
        or payload.get("response")
        or payload
    )
    model = payload.get("model") if isinstance(payload.get("model"), str) else None
    usage = payload.get("usage") if isinstance(payload.get("usage"), Mapping) else None
    return StaticImageResponse(text=text, raw=payload, model=model, usage=usage)


def normalize_visual_understanding_response(payload: Mapping[str, Any]) -> VisualUnderstandingResponse:
    text = _coerce_text(
        payload.get("text")
        or payload.get("output")
        or payload.get("content")
        or payload.get("result")
        or payload.get("response")
        or payload
    )
    model = payload.get("model") if isinstance(payload.get("model"), str) else None
    usage = payload.get("usage") if isinstance(payload.get("usage"), Mapping) else None
    objects = payload.get("objects") if isinstance(payload.get("objects"), list) else None
    labels = payload.get("labels") if isinstance(payload.get("labels"), list) else None
    if labels is not None:
        labels = [str(item) for item in labels]
    return VisualUnderstandingResponse(text=text, raw=payload, model=model, usage=usage, objects=objects, labels=labels)


def normalize_vision_response(payload: Mapping[str, Any], kind: str) -> VisionResponse:
    normalized_kind = kind.strip().lower()
    if normalized_kind in {"static image", "static_image", "image", "still image"}:
        return normalize_static_image_response(payload)
    if normalized_kind in {"visual understanding", "visual_understanding", "vision", "analysis"}:
        return normalize_visual_understanding_response(payload)
    raise ValueError(f"Unsupported vision kind: {kind}")
