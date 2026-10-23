from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


@dataclass
class StaticImageRequest:
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    mime_type: Optional[str] = None
    prompt: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = dict(self.extra)
        if self.image_url is not None:
            payload["image_url"] = self.image_url
        if self.image_base64 is not None:
            payload["image_base64"] = self.image_base64
        if self.mime_type is not None:
            payload["mime_type"] = self.mime_type
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        return payload


@dataclass
class VisualUnderstandingRequest:
    images: Sequence[Union[str, Mapping[str, Any]]] = field(default_factory=list)
    prompt: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = dict(self.extra)
        payload["images"] = [normalize_image_item(item) for item in self.images]
        payload["prompt"] = self.prompt
        return payload


@dataclass
class StaticImageResponse:
    raw: Dict[str, Any]
    text: str = ""
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualUnderstandingResponse:
    raw: Dict[str, Any]
    summary: str = ""
    labels: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)


def normalize_image_item(item: Union[str, Mapping[str, Any]]) -> Dict[str, Any]:
    if isinstance(item, str):
        if item.startswith("http://") or item.startswith("https://"):
            return {"image_url": item}
        return {"image_base64": item}
    return dict(item)


def normalize_static_image_response(raw: Mapping[str, Any]) -> StaticImageResponse:
    payload = dict(raw)
    text = _extract_text(payload)
    return StaticImageResponse(raw=payload, text=text, data=payload)


def normalize_visual_understanding_response(raw: Mapping[str, Any]) -> VisualUnderstandingResponse:
    payload = dict(raw)
    summary = _extract_text(payload)
    labels = _extract_labels(payload)
    return VisualUnderstandingResponse(raw=payload, summary=summary, labels=labels, data=payload)


def _extract_text(payload: Mapping[str, Any]) -> str:
    for key in ("text", "summary", "caption", "response", "content"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    output = payload.get("output")
    if isinstance(output, str):
        return output
    if isinstance(output, Sequence) and not isinstance(output, (str, bytes, bytearray)):
        pieces: List[str] = []
        for item in output:
            if isinstance(item, Mapping):
                text = item.get("text") or item.get("content")
                if isinstance(text, str) and text:
                    pieces.append(text)
        return "\n".join(pieces)
    return ""


def _extract_labels(payload: Mapping[str, Any]) -> List[str]:
    labels = payload.get("labels")
    if isinstance(labels, Sequence) and not isinstance(labels, (str, bytes, bytearray)):
        return [label for label in labels if isinstance(label, str) and label]
    objects = payload.get("objects")
    if isinstance(objects, Sequence) and not isinstance(objects, (str, bytes, bytearray)):
        extracted: List[str] = []
        for obj in objects:
            if isinstance(obj, Mapping):
                name = obj.get("label") or obj.get("name")
                if isinstance(name, str) and name:
                    extracted.append(name)
        return extracted
    return []
