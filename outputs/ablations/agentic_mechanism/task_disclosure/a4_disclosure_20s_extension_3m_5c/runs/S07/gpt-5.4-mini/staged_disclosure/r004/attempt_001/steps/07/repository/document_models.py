from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class OCRRequest:
    image_url: str
    language: Optional[str] = None
    include_confidence: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OCRWord:
    text: str
    confidence: Optional[float] = None
    bbox: Optional[Tuple[float, float, float, float]] = None


@dataclass(frozen=True)
class OCRLine:
    text: str
    words: Sequence[OCRWord] = field(default_factory=tuple)
    confidence: Optional[float] = None


@dataclass(frozen=True)
class OCRResponse:
    text: str
    words: Sequence[OCRWord] = field(default_factory=tuple)
    lines: Sequence[OCRLine] = field(default_factory=tuple)
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LayoutRequest:
    image_url: str
    detect_tables: bool = True
    detect_reading_order: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LayoutBlock:
    block_type: str
    text: str = ""
    bbox: Optional[Tuple[float, float, float, float]] = None
    confidence: Optional[float] = None
    children: Sequence["LayoutBlock"] = field(default_factory=tuple)


@dataclass(frozen=True)
class LayoutResponse:
    blocks: Sequence[LayoutBlock] = field(default_factory=tuple)
    page_size: Optional[Tuple[float, float]] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_bbox(value: Any) -> Optional[Tuple[float, float, float, float]]:
    if value is None:
        return None
    if isinstance(value, dict):
        keys = ["left", "top", "right", "bottom"]
        if all(k in value for k in keys):
            return tuple(float(value[k]) for k in keys)  # type: ignore[return-value]
        keys = ["x", "y", "width", "height"]
        if all(k in value for k in keys):
            x = float(value["x"])
            y = float(value["y"])
            w = float(value["width"])
            h = float(value["height"])
            return (x, y, x + w, y + h)
        return None
    if isinstance(value, (list, tuple)) and len(value) == 4:
        return tuple(float(v) for v in value)  # type: ignore[return-value]
    return None


def normalize_ocr_word(value: Any) -> OCRWord:
    if isinstance(value, OCRWord):
        return value
    text = str(value.get("text", "")) if isinstance(value, dict) else str(value)
    confidence = None
    bbox = None
    if isinstance(value, dict):
        conf = value.get("confidence")
        confidence = float(conf) if conf is not None else None
        bbox = normalize_bbox(value.get("bbox") or value.get("bounding_box") or value.get("box"))
    return OCRWord(text=text, confidence=confidence, bbox=bbox)


def normalize_ocr_line(value: Any) -> OCRLine:
    if isinstance(value, OCRLine):
        return value
    if isinstance(value, dict):
        words = tuple(normalize_ocr_word(w) for w in value.get("words", []))
        return OCRLine(
            text=str(value.get("text", "")),
            words=words,
            confidence=float(value["confidence"]) if value.get("confidence") is not None else None,
        )
    return OCRLine(text=str(value))


def normalize_ocr_response(value: Any) -> OCRResponse:
    if isinstance(value, OCRResponse):
        return value
    if not isinstance(value, dict):
        return OCRResponse(text=str(value), raw={"value": value})
    words = tuple(normalize_ocr_word(w) for w in value.get("words", []))
    lines = tuple(normalize_ocr_line(l) for l in value.get("lines", []))
    confidence = value.get("confidence")
    return OCRResponse(
        text=str(value.get("text", "")),
        words=words,
        lines=lines,
        confidence=float(confidence) if confidence is not None else None,
        raw=value,
    )


def normalize_layout_block(value: Any) -> LayoutBlock:
    if isinstance(value, LayoutBlock):
        return value
    if isinstance(value, dict):
        children = tuple(normalize_layout_block(c) for c in value.get("children", []))
        confidence = value.get("confidence")
        return LayoutBlock(
            block_type=str(value.get("block_type", value.get("type", "unknown"))),
            text=str(value.get("text", "")),
            bbox=normalize_bbox(value.get("bbox") or value.get("bounding_box") or value.get("box")),
            confidence=float(confidence) if confidence is not None else None,
            children=children,
        )
    return LayoutBlock(block_type=str(value))


def normalize_layout_response(value: Any) -> LayoutResponse:
    if isinstance(value, LayoutResponse):
        return value
    if not isinstance(value, dict):
        return LayoutResponse(raw={"value": value})
    blocks = tuple(normalize_layout_block(b) for b in value.get("blocks", []))
    page_size = normalize_bbox(value.get("page_size"))
    if page_size is not None:
        page_size = (page_size[2] - page_size[0], page_size[3] - page_size[1])
    return LayoutResponse(blocks=blocks, page_size=page_size, raw=value)
