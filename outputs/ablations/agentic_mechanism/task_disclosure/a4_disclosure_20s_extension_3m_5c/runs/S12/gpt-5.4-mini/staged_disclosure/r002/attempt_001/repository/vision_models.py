from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


@dataclass
class StaticImageRequest:
    image: str
    prompt: str
    model: Optional[str] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "image": self.image,
            "prompt": self.prompt,
        }
        if self.model is not None:
            payload["model"] = self.model
        if self.max_output_tokens is not None:
            payload["max_output_tokens"] = self.max_output_tokens
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.extra:
            payload.update(self.extra)
        return payload


@dataclass
class VisualUnderstandingRequest:
    images: Sequence[str]
    prompt: str
    model: Optional[str] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "images": list(self.images),
            "prompt": self.prompt,
        }
        if self.model is not None:
            payload["model"] = self.model
        if self.max_output_tokens is not None:
            payload["max_output_tokens"] = self.max_output_tokens
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.extra:
            payload.update(self.extra)
        return payload


@dataclass
class VisionResponse:
    text: str
    model: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "VisionResponse":
        text = normalize_vision_output(raw)
        model = raw.get("model") if isinstance(raw, Mapping) else None
        usage = raw.get("usage") if isinstance(raw, Mapping) else None
        metadata: Dict[str, Any] = {}
        for key in ("id", "created", "object", "finish_reason"):
            if key in raw:
                metadata[key] = raw[key]
        return cls(text=text, model=model, raw=dict(raw), usage=dict(usage) if isinstance(usage, Mapping) else usage, metadata=metadata)


def normalize_vision_output(data: Any) -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, Mapping):
        for key in ("text", "output_text", "content", "answer", "result"):
            value = data.get(key)
            normalized = normalize_vision_output(value)
            if normalized:
                return normalized
        choices = data.get("choices")
        if isinstance(choices, Sequence) and not isinstance(choices, (str, bytes, bytearray)):
            for choice in choices:
                normalized = normalize_vision_output(choice)
                if normalized:
                    return normalized
        message = data.get("message")
        if isinstance(message, Mapping):
            normalized = normalize_vision_output(message.get("content"))
            if normalized:
                return normalized
        content = data.get("content")
        if isinstance(content, Sequence) and not isinstance(content, (str, bytes, bytearray)):
            parts: List[str] = []
            for part in content:
                if isinstance(part, Mapping):
                    text = part.get("text") or part.get("content")
                    if isinstance(text, str) and text.strip():
                        parts.append(text.strip())
                elif isinstance(part, str) and part.strip():
                    parts.append(part.strip())
            if parts:
                return "\n".join(parts)
    if isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
        parts = [normalize_vision_output(item) for item in data]
        parts = [part for part in parts if part]
        if parts:
            return "\n".join(parts)
    return str(data).strip()


def normalize_static_image_response(data: Any) -> VisionResponse:
    if isinstance(data, VisionResponse):
        return data
    if isinstance(data, Mapping):
        return VisionResponse.from_raw(data)
    return VisionResponse(text=normalize_vision_output(data), raw={"value": data})


def normalize_visual_understanding_response(data: Any) -> VisionResponse:
    return normalize_static_image_response(data)
