from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


@dataclass
class BoundingBox:
    left: float
    top: float
    right: float
    bottom: float

    @classmethod
    def from_any(cls, value: Any) -> Optional["BoundingBox"]:
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            if {"left", "top", "right", "bottom"}.issubset(value.keys()):
                return cls(
                    left=float(value["left"]),
                    top=float(value["top"]),
                    right=float(value["right"]),
                    bottom=float(value["bottom"]),
                )
            if {"x", "y", "width", "height"}.issubset(value.keys()):
                x = float(value["x"])
                y = float(value["y"])
                w = float(value["width"])
                h = float(value["height"])
                return cls(left=x, top=y, right=x + w, bottom=y + h)
        if isinstance(value, Sequence) and len(value) == 4:
            a, b, c, d = value
            return cls(left=float(a), top=float(b), right=float(c), bottom=float(d))
        return None

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class OCRTextSpan:
    text: str
    bounding_box: Optional[BoundingBox] = None
    confidence: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRTextSpan":
        return cls(
            text=str(data.get("text", "")),
            bounding_box=BoundingBox.from_any(data.get("bounding_box") or data.get("bbox") or data.get("box")),
            confidence=_optional_float(data.get("confidence") or data.get("score")),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {"text": self.text}
        if self.bounding_box is not None:
            payload["bounding_box"] = self.bounding_box.to_dict()
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        return payload


@dataclass
class OCRLine:
    text: str
    spans: List[OCRTextSpan] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None
    confidence: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRLine":
        spans = [OCRTextSpan.from_dict(item) for item in data.get("spans", []) if isinstance(item, dict)]
        return cls(
            text=str(data.get("text", "")),
            spans=spans,
            bounding_box=BoundingBox.from_any(data.get("bounding_box") or data.get("bbox") or data.get("box")),
            confidence=_optional_float(data.get("confidence") or data.get("score")),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {"text": self.text, "spans": [span.to_dict() for span in self.spans]}
        if self.bounding_box is not None:
            payload["bounding_box"] = self.bounding_box.to_dict()
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        return payload


@dataclass
class OCRPage:
    page_number: int
    text: str = ""
    lines: List[OCRLine] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None
    width: Optional[float] = None
    height: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRPage":
        lines = [OCRLine.from_dict(item) for item in data.get("lines", []) if isinstance(item, dict)]
        return cls(
            page_number=int(data.get("page_number", data.get("page", 0))),
            text=str(data.get("text", "")),
            lines=lines,
            bounding_box=BoundingBox.from_any(data.get("bounding_box") or data.get("bbox") or data.get("box")),
            width=_optional_float(data.get("width")),
            height=_optional_float(data.get("height")),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "page_number": self.page_number,
            "text": self.text,
            "lines": [line.to_dict() for line in self.lines],
        }
        if self.bounding_box is not None:
            payload["bounding_box"] = self.bounding_box.to_dict()
        if self.width is not None:
            payload["width"] = self.width
        if self.height is not None:
            payload["height"] = self.height
        return payload


@dataclass
class OCRDocument:
    text: str = ""
    pages: List[OCRPage] = field(default_factory=list)
    language: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRDocument":
        pages = [OCRPage.from_dict(item) for item in data.get("pages", []) if isinstance(item, dict)]
        return cls(
            text=str(data.get("text", "")),
            pages=pages,
            language=data.get("language"),
            confidence=_optional_float(data.get("confidence") or data.get("score")),
            metadata=dict(data.get("metadata", {})) if isinstance(data.get("metadata"), dict) else {},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "text": self.text,
            "pages": [page.to_dict() for page in self.pages],
            "metadata": dict(self.metadata),
        }
        if self.language is not None:
            payload["language"] = self.language
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        return payload


@dataclass
class LayoutElement:
    type: str
    text: str = ""
    bounding_box: Optional[BoundingBox] = None
    page_number: Optional[int] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutElement":
        return cls(
            type=str(data.get("type", data.get("kind", "unknown"))),
            text=str(data.get("text", "")),
            bounding_box=BoundingBox.from_any(data.get("bounding_box") or data.get("bbox") or data.get("box")),
            page_number=_optional_int(data.get("page_number") or data.get("page")),
            confidence=_optional_float(data.get("confidence") or data.get("score")),
            metadata=dict(data.get("metadata", {})) if isinstance(data.get("metadata"), dict) else {},
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {"type": self.type, "text": self.text, "metadata": dict(self.metadata)}
        if self.bounding_box is not None:
            payload["bounding_box"] = self.bounding_box.to_dict()
        if self.page_number is not None:
            payload["page_number"] = self.page_number
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        return payload


@dataclass
class LayoutDocument:
    elements: List[LayoutElement] = field(default_factory=list)
    pages: List[OCRPage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutDocument":
        elements = [LayoutElement.from_dict(item) for item in data.get("elements", []) if isinstance(item, dict)]
        pages = [OCRPage.from_dict(item) for item in data.get("pages", []) if isinstance(item, dict)]
        return cls(
            elements=elements,
            pages=pages,
            metadata=dict(data.get("metadata", {})) if isinstance(data.get("metadata"), dict) else {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "elements": [element.to_dict() for element in self.elements],
            "pages": [page.to_dict() for page in self.pages],
            "metadata": dict(self.metadata),
        }


@dataclass
class OCRRequest:
    image: Optional[bytes] = None
    image_url: Optional[str] = None
    language: Optional[str] = None
    normalize: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutExtractionRequest:
    image: Optional[bytes] = None
    image_url: Optional[str] = None
    include_lines: bool = True
    include_tables: bool = True
    include_blocks: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_ocr_document(data: Union[OCRDocument, Dict[str, Any], str]) -> OCRDocument:
    if isinstance(data, OCRDocument):
        return data
    if isinstance(data, str):
        return OCRDocument(text=data, pages=[])
    if not isinstance(data, dict):
        return OCRDocument(text=str(data), pages=[])
    return OCRDocument.from_dict(data)


def normalize_layout_document(data: Union[LayoutDocument, Dict[str, Any]]) -> LayoutDocument:
    if isinstance(data, LayoutDocument):
        return data
    if not isinstance(data, dict):
        return LayoutDocument()
    return LayoutDocument.from_dict(data)


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return _collapse_whitespace(text)
    if isinstance(text, (list, tuple)):
        return _collapse_whitespace("\n".join(normalize_text(item) for item in text if item is not None))
    if isinstance(text, dict):
        if "text" in text:
            return normalize_text(text["text"])
        if "lines" in text:
            return normalize_text([item.get("text", "") for item in text.get("lines", []) if isinstance(item, dict)])
    return _collapse_whitespace(str(text))


def _collapse_whitespace(value: str) -> str:
    return " ".join(value.replace("\r\n", "\n").replace("\r", "\n").split())


def _optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _optional_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
