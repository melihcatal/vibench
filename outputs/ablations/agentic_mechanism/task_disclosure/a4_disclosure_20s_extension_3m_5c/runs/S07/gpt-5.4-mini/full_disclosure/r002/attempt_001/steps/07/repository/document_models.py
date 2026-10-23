from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple


BBox = Tuple[float, float, float, float]


def _coerce_bbox(value: Any) -> Optional[BBox]:
    if value is None:
        return None
    if isinstance(value, dict):
        if {"x1", "y1", "x2", "y2"} <= value.keys():
            return (float(value["x1"]), float(value["y1"]), float(value["x2"]), float(value["y2"]))
        if {"left", "top", "right", "bottom"} <= value.keys():
            return (float(value["left"]), float(value["top"]), float(value["right"]), float(value["bottom"]))
    if isinstance(value, (list, tuple)) and len(value) == 4:
        return (float(value[0]), float(value[1]), float(value[2]), float(value[3]))
    return None


def _coerce_lines(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        return [str(v) for v in value if v is not None]
    return [str(value)]


def _coerce_dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


@dataclass
class OCRRequest:
    image: Optional[str] = None
    image_bytes: Optional[bytes] = None
    language: Optional[str] = None
    normalize: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"normalize": self.normalize}
        if self.image is not None:
            payload["image"] = self.image
        if self.image_bytes is not None:
            payload["image_bytes"] = self.image_bytes
        if self.language is not None:
            payload["language"] = self.language
        payload.update(self.extra)
        return payload


@dataclass
class LayoutExtractionRequest:
    document: Optional[str] = None
    document_bytes: Optional[bytes] = None
    include_text: bool = True
    include_tables: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "include_text": self.include_text,
            "include_tables": self.include_tables,
        }
        if self.document is not None:
            payload["document"] = self.document
        if self.document_bytes is not None:
            payload["document_bytes"] = self.document_bytes
        payload.update(self.extra)
        return payload


@dataclass
class OCRWord:
    text: str
    bbox: Optional[BBox] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRWord":
        return cls(
            text=str(data.get("text", "")),
            bbox=_coerce_bbox(data.get("bbox") or data.get("box") or data.get("bounding_box")),
            confidence=(float(data["confidence"]) if data.get("confidence") is not None else None),
            extra={k: v for k, v in data.items() if k not in {"text", "bbox", "box", "bounding_box", "confidence"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text}
        if self.bbox is not None:
            payload["bbox"] = self.bbox
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        payload.update(self.extra)
        return payload


@dataclass
class OCRLine:
    text: str
    words: List[OCRWord] = field(default_factory=list)
    bbox: Optional[BBox] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRLine":
        words = [OCRWord.from_dict(w) for w in data.get("words", []) if isinstance(w, dict)]
        return cls(
            text=str(data.get("text", "")),
            words=words,
            bbox=_coerce_bbox(data.get("bbox") or data.get("box") or data.get("bounding_box")),
            extra={k: v for k, v in data.items() if k not in {"text", "words", "bbox", "box", "bounding_box"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text, "words": [w.to_dict() for w in self.words]}
        if self.bbox is not None:
            payload["bbox"] = self.bbox
        payload.update(self.extra)
        return payload


@dataclass
class OCRPage:
    page_number: int
    text: str = ""
    lines: List[OCRLine] = field(default_factory=list)
    words: List[OCRWord] = field(default_factory=list)
    bbox: Optional[BBox] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRPage":
        return cls(
            page_number=int(data.get("page_number", data.get("page", 0))),
            text=str(data.get("text", "")),
            lines=[OCRLine.from_dict(v) for v in data.get("lines", []) if isinstance(v, dict)],
            words=[OCRWord.from_dict(v) for v in data.get("words", []) if isinstance(v, dict)],
            bbox=_coerce_bbox(data.get("bbox") or data.get("box") or data.get("bounding_box")),
            extra={k: v for k, v in data.items() if k not in {"page_number", "page", "text", "lines", "words", "bbox", "box", "bounding_box"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "page_number": self.page_number,
            "text": self.text,
            "lines": [line.to_dict() for line in self.lines],
            "words": [word.to_dict() for word in self.words],
        }
        if self.bbox is not None:
            payload["bbox"] = self.bbox
        payload.update(self.extra)
        return payload


@dataclass
class OCRResult:
    text: str = ""
    pages: List[OCRPage] = field(default_factory=list)
    language: Optional[str] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRResult":
        return cls(
            text=str(data.get("text", "")),
            pages=[OCRPage.from_dict(v) for v in data.get("pages", []) if isinstance(v, dict)],
            language=data.get("language"),
            confidence=(float(data["confidence"]) if data.get("confidence") is not None else None),
            extra={k: v for k, v in data.items() if k not in {"text", "pages", "language", "confidence"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text, "pages": [page.to_dict() for page in self.pages]}
        if self.language is not None:
            payload["language"] = self.language
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        payload.update(self.extra)
        return payload


@dataclass
class LayoutBlock:
    block_type: str
    text: str = ""
    bbox: Optional[BBox] = None
    page_number: Optional[int] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutBlock":
        return cls(
            block_type=str(data.get("block_type", data.get("type", "unknown"))),
            text=str(data.get("text", "")),
            bbox=_coerce_bbox(data.get("bbox") or data.get("box") or data.get("bounding_box")),
            page_number=(int(data["page_number"]) if data.get("page_number") is not None else (int(data["page"]) if data.get("page") is not None else None)),
            confidence=(float(data["confidence"]) if data.get("confidence") is not None else None),
            extra={k: v for k, v in data.items() if k not in {"block_type", "type", "text", "bbox", "box", "bounding_box", "page_number", "page", "confidence"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"block_type": self.block_type, "text": self.text}
        if self.bbox is not None:
            payload["bbox"] = self.bbox
        if self.page_number is not None:
            payload["page_number"] = self.page_number
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        payload.update(self.extra)
        return payload


@dataclass
class LayoutTableCell:
    text: str = ""
    row_index: Optional[int] = None
    column_index: Optional[int] = None
    bbox: Optional[BBox] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutTableCell":
        return cls(
            text=str(data.get("text", "")),
            row_index=(int(data["row_index"]) if data.get("row_index") is not None else None),
            column_index=(int(data["column_index"]) if data.get("column_index") is not None else None),
            bbox=_coerce_bbox(data.get("bbox") or data.get("box") or data.get("bounding_box")),
            extra={k: v for k, v in data.items() if k not in {"text", "row_index", "column_index", "bbox", "box", "bounding_box"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text}
        if self.row_index is not None:
            payload["row_index"] = self.row_index
        if self.column_index is not None:
            payload["column_index"] = self.column_index
        if self.bbox is not None:
            payload["bbox"] = self.bbox
        payload.update(self.extra)
        return payload


@dataclass
class LayoutTable:
    cells: List[LayoutTableCell] = field(default_factory=list)
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    bbox: Optional[BBox] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutTable":
        return cls(
            cells=[LayoutTableCell.from_dict(v) for v in data.get("cells", []) if isinstance(v, dict)],
            row_count=(int(data["row_count"]) if data.get("row_count") is not None else None),
            column_count=(int(data["column_count"]) if data.get("column_count") is not None else None),
            bbox=_coerce_bbox(data.get("bbox") or data.get("box") or data.get("bounding_box")),
            extra={k: v for k, v in data.items() if k not in {"cells", "row_count", "column_count", "bbox", "box", "bounding_box"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"cells": [cell.to_dict() for cell in self.cells]}
        if self.row_count is not None:
            payload["row_count"] = self.row_count
        if self.column_count is not None:
            payload["column_count"] = self.column_count
        if self.bbox is not None:
            payload["bbox"] = self.bbox
        payload.update(self.extra)
        return payload


@dataclass
class LayoutResult:
    blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[LayoutTable] = field(default_factory=list)
    pages: List[OCRPage] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutResult":
        return cls(
            blocks=[LayoutBlock.from_dict(v) for v in data.get("blocks", []) if isinstance(v, dict)],
            tables=[LayoutTable.from_dict(v) for v in data.get("tables", []) if isinstance(v, dict)],
            pages=[OCRPage.from_dict(v) for v in data.get("pages", []) if isinstance(v, dict)],
            extra={k: v for k, v in data.items() if k not in {"blocks", "tables", "pages"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "blocks": [block.to_dict() for block in self.blocks],
            "tables": [table.to_dict() for table in self.tables],
            "pages": [page.to_dict() for page in self.pages],
        }
        payload.update(self.extra)
        return payload


def normalize_ocr_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        if "text" in value:
            return str(value["text"]).strip()
        if "pages" in value:
            pages = [normalize_ocr_text(page) for page in value.get("pages", [])]
            return "\n".join([p for p in pages if p])
    if isinstance(value, Sequence):
        parts = [normalize_ocr_text(v) for v in value]
        return "\n".join([p for p in parts if p])
    return str(value).strip()


def normalize_layout(value: Any) -> LayoutResult:
    if isinstance(value, LayoutResult):
        return value
    if isinstance(value, dict):
        return LayoutResult.from_dict(value)
    return LayoutResult(extra={"value": value})


def normalize_ocr_result(value: Any) -> OCRResult:
    if isinstance(value, OCRResult):
        return value
    if isinstance(value, dict):
        if "pages" in value or "text" in value:
            return OCRResult.from_dict(value)
    return OCRResult(text=normalize_ocr_text(value), extra={"value": value})


def as_lines(text: Any) -> List[str]:
    if text is None:
        return []
    if isinstance(text, str):
        return [line for line in text.splitlines() if line.strip()]
    if isinstance(text, Sequence):
        return [line for line in _coerce_lines(text) if line.strip()]
    return [str(text)]


def merge_extras(*extras: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for extra in extras:
        if extra:
            merged.update(_coerce_dict(extra))
    return merged
