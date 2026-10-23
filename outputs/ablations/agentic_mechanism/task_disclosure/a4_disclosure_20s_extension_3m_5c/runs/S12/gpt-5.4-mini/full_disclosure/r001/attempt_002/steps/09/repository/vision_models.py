from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Union


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "value", "content", "caption", "label"):
            if key in value:
                return coerce_text(value[key])
        return ""
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        parts = [coerce_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    return str(value).strip()


def coerce_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, dict):
        for key in ("items", "labels", "objects", "categories", "values"):
            if key in value:
                return coerce_str_list(value[key])
        return [coerce_text(value)] if coerce_text(value) else []
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        result: List[str] = []
        for item in value:
            text = coerce_text(item)
            if text:
                result.append(text)
        return result
    text = coerce_text(value)
    return [text] if text else []


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = coerce_text(value)
        if text:
            return text
    return ""


@dataclass(frozen=True)
class ImageRequest:
    image_path: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    timeout: int = 60


@dataclass(frozen=True)
class ImageDescriptionRequest(ImageRequest):
    prompt: str = "Write a short, one-sentence visual description of this image."


@dataclass(frozen=True)
class ImageLabelRequest(ImageRequest):
    prompt: str = "List the main labels or objects visible in this image as a concise JSON array of strings."


@dataclass(frozen=True)
class ImageTextRequest(ImageRequest):
    prompt: str = "Transcribe all visible text in this image. Return only the transcription, preserving line breaks when helpful."


@dataclass(frozen=True)
class ImageSafetyRequest(ImageRequest):
    prompt: str = (
        "Assess this image for unsafe or policy-sensitive visual content. Return a concise JSON object with keys "
        "unsafe (boolean), severity (one of low, medium, high), categories (array of strings), and rationale (string)."
    )


@dataclass(frozen=True)
class ImageDescriptionResponse:
    text: str


@dataclass(frozen=True)
class ImageLabelResponse:
    labels: List[str] = field(default_factory=list)
    raw_text: str = ""


@dataclass(frozen=True)
class ImageTextResponse:
    text: str


@dataclass(frozen=True)
class ImageSafetyResponse:
    unsafe: bool
    severity: str
    categories: List[str] = field(default_factory=list)
    rationale: str = ""


def normalize_description(value: Any) -> ImageDescriptionResponse:
    return ImageDescriptionResponse(text=_first_nonempty(value))


def normalize_labels(value: Any) -> ImageLabelResponse:
    if isinstance(value, dict):
        labels = coerce_str_list(value.get("labels") or value.get("objects") or value.get("categories") or value.get("items") or value.get("value"))
        raw_text = _first_nonempty(value.get("raw_text"), value.get("text"), value.get("content"))
        if not labels and raw_text:
            labels = [line.strip("-• \t") for line in raw_text.splitlines() if line.strip()]
        return ImageLabelResponse(labels=labels, raw_text=raw_text)
    raw_text = _first_nonempty(value)
    labels = [line.strip("-• \t") for line in raw_text.splitlines() if line.strip()] if raw_text else []
    return ImageLabelResponse(labels=labels, raw_text=raw_text)


def normalize_text(value: Any) -> ImageTextResponse:
    return ImageTextResponse(text=_first_nonempty(value))


def normalize_safety(value: Any) -> ImageSafetyResponse:
    if isinstance(value, dict):
        unsafe = bool(value.get("unsafe", False))
        severity = _first_nonempty(value.get("severity")) or "low"
        categories = coerce_str_list(value.get("categories"))
        rationale = _first_nonempty(value.get("rationale"), value.get("text"), value.get("content"))
        return ImageSafetyResponse(unsafe=unsafe, severity=severity, categories=categories, rationale=rationale)
    return ImageSafetyResponse(unsafe=False, severity="low", categories=[], rationale=_first_nonempty(value))
