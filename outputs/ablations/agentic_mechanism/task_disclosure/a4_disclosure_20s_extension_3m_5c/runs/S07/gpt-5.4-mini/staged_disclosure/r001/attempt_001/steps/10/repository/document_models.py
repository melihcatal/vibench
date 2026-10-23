from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union


Number = Union[int, float]


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


@dataclass
class BoundingBox:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    @classmethod
    def from_any(cls, value: Any) -> "BoundingBox":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                x=_to_float(value.get("x", value.get("left", 0.0))),
                y=_to_float(value.get("y", value.get("top", 0.0))),
                width=_to_float(value.get("width", value.get("w", 0.0))),
                height=_to_float(value.get("height", value.get("h", 0.0))),
            )
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)) and len(value) >= 4:
            return cls(x=_to_float(value[0]), y=_to_float(value[1]), width=_to_float(value[2]), height=_to_float(value[3]))
        return cls()

    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}


@dataclass
class OCRWord:
    text: str = ""
    confidence: float = 0.0
    bbox: BoundingBox = field(default_factory=BoundingBox)

    @classmethod
    def from_any(cls, value: Any) -> "OCRWord":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                text=str(value.get("text", "")),
                confidence=_to_float(value.get("confidence", value.get("score", 0.0))),
                bbox=BoundingBox.from_any(value.get("bbox", value.get("bounding_box", value.get("box")))),
            )
        return cls(text=str(value) if value is not None else "")

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence, "bbox": self.bbox.to_dict()}


@dataclass
class OCRLine:
    text: str = ""
    words: List[OCRWord] = field(default_factory=list)
    confidence: float = 0.0
    bbox: BoundingBox = field(default_factory=BoundingBox)

    @classmethod
    def from_any(cls, value: Any) -> "OCRLine":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                text=str(value.get("text", "")),
                words=[OCRWord.from_any(item) for item in _ensure_list(value.get("words"))],
                confidence=_to_float(value.get("confidence", value.get("score", 0.0))),
                bbox=BoundingBox.from_any(value.get("bbox", value.get("bounding_box", value.get("box")))),
            )
        return cls(text=str(value) if value is not None else "")

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "words": [w.to_dict() for w in self.words], "confidence": self.confidence, "bbox": self.bbox.to_dict()}


@dataclass
class OCRPage:
    page_number: int = 0
    text: str = ""
    lines: List[OCRLine] = field(default_factory=list)
    words: List[OCRWord] = field(default_factory=list)
    width: float = 0.0
    height: float = 0.0

    @classmethod
    def from_any(cls, value: Any) -> "OCRPage":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                page_number=_to_int(value.get("page_number", value.get("page", 0))),
                text=str(value.get("text", "")),
                lines=[OCRLine.from_any(item) for item in _ensure_list(value.get("lines"))],
                words=[OCRWord.from_any(item) for item in _ensure_list(value.get("words"))],
                width=_to_float(value.get("width", 0.0)),
                height=_to_float(value.get("height", 0.0)),
            )
        return cls(text=str(value) if value is not None else "")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "text": self.text,
            "lines": [line.to_dict() for line in self.lines],
            "words": [word.to_dict() for word in self.words],
            "width": self.width,
            "height": self.height,
        }


@dataclass
class OCRRequest:
    document_id: Optional[str] = None
    url: Optional[str] = None
    content_base64: Optional[str] = None
    language: Optional[str] = None
    detect_orientation: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"detect_orientation": self.detect_orientation}
        if self.document_id is not None:
            payload["document_id"] = self.document_id
        if self.url is not None:
            payload["url"] = self.url
        if self.content_base64 is not None:
            payload["content_base64"] = self.content_base64
        if self.language is not None:
            payload["language"] = self.language
        payload.update(self.extra)
        return payload


@dataclass
class OCRResponse:
    pages: List[OCRPage] = field(default_factory=list)
    text: str = ""
    provider: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, value: Any) -> "OCRResponse":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                pages=[OCRPage.from_any(item) for item in _ensure_list(value.get("pages"))],
                text=str(value.get("text", "")),
                provider=value.get("provider"),
                raw=dict(value),
            )
        return cls(text=str(value) if value is not None else "", raw={"value": value})

    def normalized_text(self) -> str:
        if self.text:
            return self.text.strip()
        return "\n".join(page.text.strip() for page in self.pages if page.text).strip()


@dataclass
class LayoutBlock:
    block_type: str = "unknown"
    text: str = ""
    bbox: BoundingBox = field(default_factory=BoundingBox)
    confidence: float = 0.0
    page_number: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, value: Any) -> "LayoutBlock":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                block_type=str(value.get("block_type", value.get("type", "unknown"))),
                text=str(value.get("text", "")),
                bbox=BoundingBox.from_any(value.get("bbox", value.get("bounding_box", value.get("box")))),
                confidence=_to_float(value.get("confidence", value.get("score", 0.0))),
                page_number=_to_int(value.get("page_number", value.get("page", 0))),
                metadata={k: v for k, v in value.items() if k not in {"block_type", "type", "text", "bbox", "bounding_box", "box", "confidence", "score", "page_number", "page"}},
            )
        return cls(text=str(value) if value is not None else "")

    def to_dict(self) -> Dict[str, Any]:
        return {"block_type": self.block_type, "text": self.text, "bbox": self.bbox.to_dict(), "confidence": self.confidence, "page_number": self.page_number, "metadata": self.metadata}


@dataclass
class LayoutPage:
    page_number: int = 0
    blocks: List[LayoutBlock] = field(default_factory=list)
    width: float = 0.0
    height: float = 0.0

    @classmethod
    def from_any(cls, value: Any) -> "LayoutPage":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                page_number=_to_int(value.get("page_number", value.get("page", 0))),
                blocks=[LayoutBlock.from_any(item) for item in _ensure_list(value.get("blocks"))],
                width=_to_float(value.get("width", 0.0)),
                height=_to_float(value.get("height", 0.0)),
            )
        return cls()

    def to_dict(self) -> Dict[str, Any]:
        return {"page_number": self.page_number, "blocks": [block.to_dict() for block in self.blocks], "width": self.width, "height": self.height}


@dataclass
class LayoutRequest:
    document_id: Optional[str] = None
    url: Optional[str] = None
    content_base64: Optional[str] = None
    include_text: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"include_text": self.include_text}
        if self.document_id is not None:
            payload["document_id"] = self.document_id
        if self.url is not None:
            payload["url"] = self.url
        if self.content_base64 is not None:
            payload["content_base64"] = self.content_base64
        payload.update(self.extra)
        return payload


@dataclass
class LayoutResponse:
    pages: List[LayoutPage] = field(default_factory=list)
    provider: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, value: Any) -> "LayoutResponse":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                pages=[LayoutPage.from_any(item) for item in _ensure_list(value.get("pages"))],
                provider=value.get("provider"),
                raw=dict(value),
            )
        return cls(raw={"value": value})


def normalize_ocr_response(data: Any) -> OCRResponse:
    response = OCRResponse.from_any(data)
    if not response.text and response.pages:
        response.text = response.normalized_text()
    return response


def normalize_layout_response(data: Any) -> LayoutResponse:
    return LayoutResponse.from_any(data)
