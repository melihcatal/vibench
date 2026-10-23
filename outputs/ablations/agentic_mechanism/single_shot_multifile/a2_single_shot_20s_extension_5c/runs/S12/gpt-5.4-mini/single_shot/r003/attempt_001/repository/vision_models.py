import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageLabel:
    label: str
    confidence: Optional[float] = None


@dataclass
class LabelResult:
    labels: List[ImageLabel] = field(default_factory=list)
    raw_text: str = ""


@dataclass
class DescriptionResult:
    description: str
    raw_text: str = ""


@dataclass
class OCRResult:
    text: str
    lines: List[str] = field(default_factory=list)
    raw_text: str = ""


@dataclass
class SafetyResult:
    unsafe: bool
    categories: List[str] = field(default_factory=list)
    risk: str = "unknown"
    raw_text: str = ""


def _try_load_json(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        return None


def normalize_label_result(text: str) -> LabelResult:
    data = _try_load_json(text)
    labels: List[ImageLabel] = []
    if isinstance(data, dict):
        items = data.get("labels") or data.get("objects") or []
        for item in items:
            if isinstance(item, str):
                labels.append(ImageLabel(label=item))
            elif isinstance(item, dict):
                labels.append(ImageLabel(label=str(item.get("label") or item.get("name") or ""), confidence=item.get("confidence")))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                labels.append(ImageLabel(label=item))
            elif isinstance(item, dict):
                labels.append(ImageLabel(label=str(item.get("label") or item.get("name") or ""), confidence=item.get("confidence")))
    elif text.strip():
        for part in text.splitlines():
            cleaned = part.strip().lstrip("-•0123456789. ")
            if cleaned:
                labels.append(ImageLabel(label=cleaned))
    return LabelResult(labels=labels, raw_text=text)


def normalize_description_result(text: str) -> DescriptionResult:
    data = _try_load_json(text)
    if isinstance(data, dict):
        desc = str(data.get("description") or data.get("text") or text).strip()
        return DescriptionResult(description=desc, raw_text=text)
    return DescriptionResult(description=text.strip(), raw_text=text)


def normalize_ocr_result(text: str) -> OCRResult:
    data = _try_load_json(text)
    if isinstance(data, dict):
        lines = data.get("lines") or []
        if not lines and data.get("text"):
            lines = str(data["text"]).splitlines()
        return OCRResult(text=str(data.get("text") or "\n".join(lines)).strip(), lines=[str(x) for x in lines], raw_text=text)
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return OCRResult(text=text.strip(), lines=lines, raw_text=text)


def normalize_safety_result(text: str) -> SafetyResult:
    data = _try_load_json(text)
    if isinstance(data, dict):
        return SafetyResult(
            unsafe=bool(data.get("unsafe", False)),
            categories=[str(x) for x in (data.get("categories") or [])],
            risk=str(data.get("risk") or data.get("severity") or "unknown"),
            raw_text=text,
        )
    lowered = text.lower()
    unsafe = any(token in lowered for token in ["unsafe", "violence", "sexual", "self-harm", "weapon", "explicit"])
    return SafetyResult(unsafe=unsafe, categories=[], risk="high" if unsafe else "low", raw_text=text)
