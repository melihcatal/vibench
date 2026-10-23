from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple


class DocumentTask(str, Enum):
    OCR = "ocr"
    LAYOUT_EXTRACTION = "layout_extraction"


@dataclass
class BoundingBox:
    x0: float
    y0: float
    x1: float
    y1: float

    @classmethod
    def from_any(cls, value: Any) -> Optional["BoundingBox"]:
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            keys = {k.lower(): k for k in value.keys()}
            if {"x0", "y0", "x1", "y1"}.issubset(keys):
                return cls(
                    float(value[keys["x0"]]),
                    float(value[keys["y0"]]),
                    float(value[keys["x1"]]),
                    float(value[keys["y1"]]),
                )
            if {"left", "top", "right", "bottom"}.issubset(keys):
                return cls(
                    float(value[keys["left"]]),
                    float(value[keys["top"]]),
                    float(value[keys["right"]]),
                    float(value[keys["bottom"]]),
                )
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)) and len(value) == 4:
            return cls(float(value[0]), float(value[1]), float(value[2]), float(value[3]))
        return None

    def to_dict(self) -> Dict[str, float]:
        return {"x0": self.x0, "y0": self.y0, "x1": self.x1, "y1": self.y1}


@dataclass
class OCRBlock:
    text: str
    confidence: Optional[float] = None
    bbox: Optional[BoundingBox] = None
    page: Optional[int] = None
    index: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, value: Any) -> "OCRBlock":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(text=value)
        if not isinstance(value, dict):
            return cls(text=str(value))
        text = str(value.get("text", value.get("content", "")))
        confidence = value.get("confidence")
        bbox = BoundingBox.from_any(value.get("bbox") or value.get("bounding_box") or value.get("box"))
        page = value.get("page")
        index = value.get("index")
        metadata = {k: v for k, v in value.items() if k not in {"text", "content", "confidence", "bbox", "bounding_box", "box", "page", "index"}}
        return cls(text=text, confidence=float(confidence) if confidence is not None else None, bbox=bbox, page=page, index=index, metadata=metadata)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"text": self.text}
        if self.confidence is not None:
            data["confidence"] = self.confidence
        if self.bbox is not None:
            data["bbox"] = self.bbox.to_dict()
        if self.page is not None:
            data["page"] = self.page
        if self.index is not None:
            data["index"] = self.index
        if self.metadata:
            data.update(self.metadata)
        return data


@dataclass
class LayoutElement:
    type: str
    text: str = ""
    bbox: Optional[BoundingBox] = None
    confidence: Optional[float] = None
    page: Optional[int] = None
    row: Optional[int] = None
    column: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, value: Any) -> "LayoutElement":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(type="text", text=value)
        if not isinstance(value, dict):
            return cls(type="unknown", text=str(value))
        element_type = str(value.get("type", value.get("kind", "unknown")))
        text = str(value.get("text", value.get("content", "")))
        bbox = BoundingBox.from_any(value.get("bbox") or value.get("bounding_box") or value.get("box"))
        confidence = value.get("confidence")
        metadata = {
            k: v
            for k, v in value.items()
            if k not in {"type", "kind", "text", "content", "bbox", "bounding_box", "box", "confidence", "page", "row", "column"}
        }
        return cls(
            type=element_type,
            text=text,
            bbox=bbox,
            confidence=float(confidence) if confidence is not None else None,
            page=value.get("page"),
            row=value.get("row"),
            column=value.get("column"),
            metadata=metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"type": self.type, "text": self.text}
        if self.bbox is not None:
            data["bbox"] = self.bbox.to_dict()
        if self.confidence is not None:
            data["confidence"] = self.confidence
        if self.page is not None:
            data["page"] = self.page
        if self.row is not None:
            data["row"] = self.row
        if self.column is not None:
            data["column"] = self.column
        if self.metadata:
            data.update(self.metadata)
        return data


@dataclass
class DocumentRequest:
    task: DocumentTask
    document: Any
    language: Optional[str] = None
    page: Optional[int] = None
    options: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"task": self.task.value, "document": self.document}
        if self.language is not None:
            data["language"] = self.language
        if self.page is not None:
            data["page"] = self.page
        if self.options:
            data["options"] = dict(self.options)
        return data


@dataclass
class OCRResponse:
    text: str
    blocks: List[OCRBlock] = field(default_factory=list)
    pages: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any) -> "OCRResponse":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(text=value)
        if not isinstance(value, dict):
            return cls(text=str(value))
        text = str(value.get("text", value.get("content", "")))
        blocks_raw = value.get("blocks") or value.get("lines") or []
        blocks = [OCRBlock.from_any(item) for item in blocks_raw]
        pages = list(value.get("pages") or [])
        metadata = {k: v for k, v in value.items() if k not in {"text", "content", "blocks", "lines", "pages"}}
        if not text and blocks:
            text = "\n".join(block.text for block in blocks if block.text)
        return cls(text=text, blocks=blocks, pages=pages, metadata=metadata)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"text": self.text}
        if self.blocks:
            data["blocks"] = [b.to_dict() for b in self.blocks]
        if self.pages:
            data["pages"] = list(self.pages)
        if self.metadata:
            data.update(self.metadata)
        return data


@dataclass
class LayoutResponse:
    elements: List[LayoutElement] = field(default_factory=list)
    pages: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any) -> "LayoutResponse":
        if isinstance(value, cls):
            return value
        if not isinstance(value, dict):
            return cls(elements=[LayoutElement.from_any(value)])
        elements_raw = value.get("elements") or value.get("blocks") or value.get("items") or []
        elements = [LayoutElement.from_any(item) for item in elements_raw]
        pages = list(value.get("pages") or [])
        metadata = {k: v for k, v in value.items() if k not in {"elements", "blocks", "items", "pages"}}
        return cls(elements=elements, pages=pages, metadata=metadata)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"elements": [e.to_dict() for e in self.elements]}
        if self.pages:
            data["pages"] = list(self.pages)
        if self.metadata:
            data.update(self.metadata)
        return data


def normalize_ocr_output(value: Any) -> OCRResponse:
    return OCRResponse.normalize(value)


def normalize_layout_output(value: Any) -> LayoutResponse:
    return LayoutResponse.normalize(value)


def build_request(task: DocumentTask, document: Any, *, language: Optional[str] = None, page: Optional[int] = None, **options: Any) -> DocumentRequest:
    return DocumentRequest(task=task, document=document, language=language, page=page, options=options)
