from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


@dataclass(frozen=True)
class OCRRequest:
    document_id: Optional[str] = None
    language: Optional[str] = None
    page_numbers: Optional[Sequence[int]] = None
    include_confidence: bool = True
    extra: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "document_id": self.document_id,
            "language": self.language,
            "page_numbers": list(self.page_numbers) if self.page_numbers is not None else None,
            "include_confidence": self.include_confidence,
        }
        payload.update(dict(self.extra))
        return _strip_none(payload)


@dataclass(frozen=True)
class OCRWord:
    text: str
    confidence: Optional[float] = None
    bbox: Optional[Tuple[float, float, float, float]] = None


@dataclass(frozen=True)
class OCRPage:
    page_number: int
    text: str
    words: Sequence[OCRWord] = field(default_factory=tuple)
    confidence: Optional[float] = None


@dataclass(frozen=True)
class OCRResponse:
    document_id: Optional[str] = None
    pages: Sequence[OCRPage] = field(default_factory=tuple)
    text: str = ""
    language: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "OCRResponse":
        pages = tuple(_normalize_ocr_page(page) for page in data.get("pages", []))
        return cls(
            document_id=data.get("document_id"),
            pages=pages,
            text=str(data.get("text", "") or ""),
            language=data.get("language"),
        )


@dataclass(frozen=True)
class LayoutExtractionRequest:
    document_id: Optional[str] = None
    page_numbers: Optional[Sequence[int]] = None
    include_tables: bool = True
    include_figures: bool = True
    extra: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "document_id": self.document_id,
            "page_numbers": list(self.page_numbers) if self.page_numbers is not None else None,
            "include_tables": self.include_tables,
            "include_figures": self.include_figures,
        }
        payload.update(dict(self.extra))
        return _strip_none(payload)


@dataclass(frozen=True)
class LayoutBlock:
    block_id: Optional[str]
    block_type: str
    text: str = ""
    bbox: Optional[Tuple[float, float, float, float]] = None
    confidence: Optional[float] = None
    children: Sequence["LayoutBlock"] = field(default_factory=tuple)


@dataclass(frozen=True)
class LayoutExtractionResponse:
    document_id: Optional[str] = None
    blocks: Sequence[LayoutBlock] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LayoutExtractionResponse":
        blocks = tuple(_normalize_layout_block(block) for block in data.get("blocks", []))
        return cls(document_id=data.get("document_id"), blocks=blocks)


def normalize_ocr_response(data: Mapping[str, Any]) -> OCRResponse:
    if isinstance(data, OCRResponse):
        return data
    return OCRResponse.from_dict(data)


def normalize_layout_response(data: Mapping[str, Any]) -> LayoutExtractionResponse:
    if isinstance(data, LayoutExtractionResponse):
        return data
    return LayoutExtractionResponse.from_dict(data)


def _normalize_ocr_page(data: Mapping[str, Any]) -> OCRPage:
    words = tuple(_normalize_ocr_word(word) for word in data.get("words", []))
    return OCRPage(
        page_number=int(data.get("page_number", 0)),
        text=str(data.get("text", "") or ""),
        words=words,
        confidence=_optional_float(data.get("confidence")),
    )


def _normalize_ocr_word(data: Mapping[str, Any]) -> OCRWord:
    bbox = data.get("bbox")
    normalized_bbox = _normalize_bbox(bbox) if bbox is not None else None
    return OCRWord(
        text=str(data.get("text", "") or ""),
        confidence=_optional_float(data.get("confidence")),
        bbox=normalized_bbox,
    )


def _normalize_layout_block(data: Mapping[str, Any]) -> LayoutBlock:
    children = tuple(_normalize_layout_block(child) for child in data.get("children", []))
    bbox = data.get("bbox")
    normalized_bbox = _normalize_bbox(bbox) if bbox is not None else None
    return LayoutBlock(
        block_id=data.get("block_id"),
        block_type=str(data.get("block_type", "") or ""),
        text=str(data.get("text", "") or ""),
        bbox=normalized_bbox,
        confidence=_optional_float(data.get("confidence")),
        children=children,
    )


def _normalize_bbox(value: Any) -> Tuple[float, float, float, float]:
    if isinstance(value, (list, tuple)) and len(value) == 4:
        return (float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    if isinstance(value, Mapping):
        return (
            float(value.get("x0", value.get("left", 0.0))),
            float(value.get("y0", value.get("top", 0.0))),
            float(value.get("x1", value.get("right", 0.0))),
            float(value.get("y1", value.get("bottom", 0.0))),
        )
    raise TypeError("bbox must be a sequence of four numbers or a mapping")


def _optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value)


def _strip_none(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}
