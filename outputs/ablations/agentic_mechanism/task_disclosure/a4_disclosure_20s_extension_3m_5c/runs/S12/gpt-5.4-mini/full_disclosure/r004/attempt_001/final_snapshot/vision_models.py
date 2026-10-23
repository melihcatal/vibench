import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


def _coerce_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _extract_json_payload(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    text = _normalize_text(value)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


@dataclass(frozen=True)
class VisionImageRequest:
    image_path: str
    prompt: Optional[str] = None
    max_items: Optional[int] = None
    model: Optional[str] = None
    temperature: Optional[float] = None


@dataclass(frozen=True)
class VisionTextRequest:
    image_path: str
    max_lines: int = 20
    model: Optional[str] = None
    temperature: Optional[float] = None


@dataclass(frozen=True)
class VisionLabelRequest:
    image_path: str
    max_labels: int = 10
    model: Optional[str] = None
    temperature: Optional[float] = None


@dataclass(frozen=True)
class VisionSafetyRequest:
    image_path: str
    model: Optional[str] = None
    temperature: Optional[float] = None


@dataclass(frozen=True)
class VisionDescriptionResponse:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VisionLabelsResponse:
    labels: List[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VisionTextResponse:
    lines: List[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VisionSafetyResponse:
    safe: bool
    score: float
    categories: List[str]
    rationale: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_description_result(result: Any) -> VisionDescriptionResponse:
    raw = result if isinstance(result, dict) else {}
    if isinstance(result, str):
        return VisionDescriptionResponse(text=_normalize_text(result), raw=raw)
    if isinstance(result, Mapping):
        text = _normalize_text(result.get("text") or result.get("description") or result.get("content") or result.get("message"))
        if not text and result.get("choices"):
            try:
                text = _normalize_text(result["choices"][0]["message"]["content"])
            except Exception:
                text = ""
        return VisionDescriptionResponse(text=text, raw=dict(result))
    return VisionDescriptionResponse(text=_normalize_text(result), raw=raw)


def normalize_labels_result(result: Any) -> VisionLabelsResponse:
    raw = result if isinstance(result, dict) else {}
    payload = _extract_json_payload(result)
    if isinstance(payload, list):
        return VisionLabelsResponse(labels=_coerce_str_list(payload), raw=raw)
    if isinstance(result, Mapping):
        labels = result.get("labels") or result.get("objects") or result.get("items")
        if labels is None and result.get("choices"):
            try:
                labels = _extract_json_payload(result["choices"][0]["message"]["content"])
            except Exception:
                labels = None
        return VisionLabelsResponse(labels=_coerce_str_list(labels), raw=dict(result))
    return VisionLabelsResponse(labels=_coerce_str_list(payload), raw=raw)


def normalize_text_result(result: Any) -> VisionTextResponse:
    raw = result if isinstance(result, dict) else {}
    payload = _extract_json_payload(result)
    if isinstance(payload, list):
        return VisionTextResponse(lines=_coerce_str_list(payload), raw=raw)
    if isinstance(result, Mapping):
        lines = result.get("lines") or result.get("text") or result.get("transcript")
        if lines is None and result.get("choices"):
            try:
                lines = _extract_json_payload(result["choices"][0]["message"]["content"])
            except Exception:
                lines = None
        return VisionTextResponse(lines=_coerce_str_list(lines), raw=dict(result))
    return VisionTextResponse(lines=_coerce_str_list(payload), raw=raw)


def normalize_safety_result(result: Any) -> VisionSafetyResponse:
    raw = result if isinstance(result, dict) else {}
    payload = _extract_json_payload(result)
    data = payload if isinstance(payload, Mapping) else result if isinstance(result, Mapping) else {}
    safe = bool(data.get("safe", False)) if isinstance(data, Mapping) else False
    score = float(data.get("score", 0.0)) if isinstance(data, Mapping) and data.get("score") is not None else 0.0
    categories = _coerce_str_list(data.get("categories") if isinstance(data, Mapping) else None)
    rationale = _normalize_text(data.get("rationale") if isinstance(data, Mapping) else None)
    return VisionSafetyResponse(safe=safe, score=score, categories=categories, rationale=rationale, raw=dict(result) if isinstance(result, Mapping) else raw)
