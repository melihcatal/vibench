from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _normalize_bbox(value: Any) -> Tuple[float, float, float, float]:
    if isinstance(value, dict):
        return (
            _as_float(value.get("x", value.get("left", 0.0))),
            _as_float(value.get("y", value.get("top", 0.0))),
            _as_float(value.get("width", value.get("w", 0.0))),
            _as_float(value.get("height", value.get("h", 0.0))),
        )
    if isinstance(value, (list, tuple)) and len(value) >= 4:
        return (_as_float(value[0]), _as_float(value[1]), _as_float(value[2]), _as_float(value[3]))
    return (0.0, 0.0, 0.0, 0.0)


@dataclass
class OCRRequest:
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    language: Optional[str] = None
    page_number: int = 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRRequest":
        return cls(
            image_url=data.get("image_url"),
            image_base64=data.get("image_base64"),
            language=data.get("language"),
            page_number=_as_int(data.get("page_number", 1), 1),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"page_number": self.page_number}
        if self.image_url is not None:
            payload["image_url"] = self.image_url
        if self.image_base64 is not None:
            payload["image_base64"] = self.image_base64
        if self.language is not None:
            payload["language"] = self.language
        return payload


@dataclass
class OCRWord:
    text: str
    confidence: float = 0.0
    bbox: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRWord":
        return cls(
            text=_as_str(data.get("text")),
            confidence=_as_float(data.get("confidence", 0.0)),
            bbox=_normalize_bbox(data.get("bbox", data.get("box"))),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence, "bbox": list(self.bbox)}


@dataclass
class OCRLine:
    text: str
    confidence: float = 0.0
    words: List[OCRWord] = field(default_factory=list)
    bbox: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRLine":
        return cls(
            text=_as_str(data.get("text")),
            confidence=_as_float(data.get("confidence", 0.0)),
            words=[OCRWord.from_dict(item) for item in data.get("words", []) or []],
            bbox=_normalize_bbox(data.get("bbox", data.get("box"))),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "words": [word.to_dict() for word in self.words],
            "bbox": list(self.bbox),
        }


@dataclass
class OCRResponse:
    text: str = ""
    language: Optional[str] = None
    confidence: float = 0.0
    words: List[OCRWord] = field(default_factory=list)
    lines: List[OCRLine] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OCRResponse":
        return cls(
            text=_as_str(data.get("text")),
            language=data.get("language"),
            confidence=_as_float(data.get("confidence", 0.0)),
            words=[OCRWord.from_dict(item) for item in data.get("words", []) or []],
            lines=[OCRLine.from_dict(item) for item in data.get("lines", []) or []],
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text, "confidence": self.confidence}
        if self.language is not None:
            payload["language"] = self.language
        if self.words:
            payload["words"] = [word.to_dict() for word in self.words]
        if self.lines:
            payload["lines"] = [line.to_dict() for line in self.lines]
        return payload


@dataclass
class LayoutRequest:
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    include_text: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutRequest":
        return cls(
            image_url=data.get("image_url"),
            image_base64=data.get("image_base64"),
            include_text=bool(data.get("include_text", True)),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"include_text": self.include_text}
        if self.image_url is not None:
            payload["image_url"] = self.image_url
        if self.image_base64 is not None:
            payload["image_base64"] = self.image_base64
        return payload


@dataclass
class LayoutBlock:
    block_type: str
    text: str = ""
    confidence: float = 0.0
    bbox: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    children: List["LayoutBlock"] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutBlock":
        return cls(
            block_type=_as_str(data.get("block_type", data.get("type", ""))),
            text=_as_str(data.get("text")),
            confidence=_as_float(data.get("confidence", 0.0)),
            bbox=_normalize_bbox(data.get("bbox", data.get("box"))),
            children=[cls.from_dict(item) for item in data.get("children", []) or []],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_type": self.block_type,
            "text": self.text,
            "confidence": self.confidence,
            "bbox": list(self.bbox),
            "children": [child.to_dict() for child in self.children],
        }


@dataclass
class LayoutResponse:
    blocks: List[LayoutBlock] = field(default_factory=list)
    page_count: int = 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutResponse":
        return cls(
            blocks=[LayoutBlock.from_dict(item) for item in data.get("blocks", []) or []],
            page_count=_as_int(data.get("page_count", 1), 1),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"blocks": [block.to_dict() for block in self.blocks], "page_count": self.page_count}


def normalize_ocr_response(data: Dict[str, Any]) -> OCRResponse:
    return OCRResponse.from_dict(data)


def normalize_layout_response(data: Dict[str, Any]) -> LayoutResponse:
    return LayoutResponse.from_dict(data)
