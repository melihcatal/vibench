from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


@dataclass
class StaticImageRequest:
    image_url: str
    prompt: Optional[str] = None
    model: Optional[str] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualUnderstandingRequest:
    image_urls: Sequence[str]
    prompt: str
    model: Optional[str] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedVisionResult:
    text: str
    model: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


def _coerce_message_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("text", "content", "value", "caption", "description"):
            if key in value and value[key] is not None:
                return _coerce_message_text(value[key])
        return ""
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        parts: List[str] = []
        for item in value:
            part = _coerce_message_text(item)
            if part:
                parts.append(part)
        return "\n".join(parts)
    return str(value)


def build_static_image_request_payload(request: StaticImageRequest) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "image_url": request.image_url,
    }
    if request.prompt is not None:
        payload["prompt"] = request.prompt
    if request.model is not None:
        payload["model"] = request.model
    if request.max_output_tokens is not None:
        payload["max_output_tokens"] = request.max_output_tokens
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    payload.update(request.extra)
    return payload


def build_visual_understanding_request_payload(request: VisualUnderstandingRequest) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "image_urls": list(request.image_urls),
        "prompt": request.prompt,
    }
    if request.model is not None:
        payload["model"] = request.model
    if request.max_output_tokens is not None:
        payload["max_output_tokens"] = request.max_output_tokens
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    payload.update(request.extra)
    return payload


def normalize_vision_response(response: Any) -> NormalizedVisionResult:
    if isinstance(response, NormalizedVisionResult):
        return response

    model = None
    usage: Dict[str, Any] = {}
    text = ""

    if isinstance(response, Mapping):
        model = response.get("model") or response.get("model_name")
        usage_value = response.get("usage")
        if isinstance(usage_value, Mapping):
            usage = dict(usage_value)

        if "text" in response:
            text = _coerce_message_text(response.get("text"))
        elif "content" in response:
            text = _coerce_message_text(response.get("content"))
        elif "output_text" in response:
            text = _coerce_message_text(response.get("output_text"))
        elif "choices" in response:
            choices = response.get("choices")
            if isinstance(choices, Sequence):
                for choice in choices:
                    if isinstance(choice, Mapping):
                        if "message" in choice:
                            text = _coerce_message_text(choice.get("message"))
                            if text:
                                break
                        if "text" in choice:
                            text = _coerce_message_text(choice.get("text"))
                            if text:
                                break
        else:
            text = _coerce_message_text(response)
    else:
        text = _coerce_message_text(response)

    return NormalizedVisionResult(text=text, model=model, usage=usage, raw=response)
