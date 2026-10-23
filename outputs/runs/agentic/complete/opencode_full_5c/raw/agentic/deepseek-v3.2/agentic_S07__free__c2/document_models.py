from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import json


class DocumentType(Enum):
    """Types of documents that can be processed."""

    IMAGE = "image"
    PDF = "pdf"
    SCANNED_DOCUMENT = "scanned_document"
    FORM = "form"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    CONTRACT = "contract"


class ProcessingStatus(Enum):
    """Status of document processing."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class BoundingBox:
    """Bounding box coordinates."""

    x: float
    y: float
    width: float
    height: float

    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "BoundingBox":
        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            width=data.get("width", 0),
            height=data.get("height", 0),
        )


@dataclass
class TextElement:
    """Base class for text elements."""

    text: str
    confidence: float
    bounding_box: BoundingBox

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box.to_dict(),
        }


@dataclass
class Word(TextElement):
    """Word element."""

    pass


@dataclass
class Line(TextElement):
    """Line element containing words."""

    words: List[Word] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict["words"] = [word.to_dict() for word in self.words]
        return base_dict


@dataclass
class Paragraph(TextElement):
    """Paragraph element containing lines."""

    lines: List[Line] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict["lines"] = [line.to_dict() for line in self.lines]
        return base_dict


@dataclass
class TableCell:
    """Table cell element."""

    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    text: str = ""
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "row_index": self.row_index,
            "column_index": self.column_index,
            "row_span": self.row_span,
            "column_span": self.column_span,
            "text": self.text,
            "confidence": self.confidence,
        }
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box.to_dict()
        return result


@dataclass
class Table:
    """Table structure."""

    cells: List[TableCell] = field(default_factory=list)
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "cells": [cell.to_dict() for cell in self.cells],
            "confidence": self.confidence,
        }
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box.to_dict()

        if self.cells:
            max_row = max(cell.row_index for cell in self.cells)
            max_col = max(cell.column_index for cell in self.cells)
            result["dimensions"] = {"rows": max_row, "columns": max_col}

        return result


@dataclass
class KeyValuePair:
    """Key-value pair from form-like document."""

    key: str
    value: str
    confidence: float
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"key": self.key, "value": self.value, "confidence": self.confidence}
        if self.key_bounding_box:
            result["key_bounding_box"] = self.key_bounding_box.to_dict()
        if self.value_bounding_box:
            result["value_bounding_box"] = self.value_bounding_box.to_dict()
        return result


@dataclass
class DocumentPage:
    """Single page of a document."""

    page_number: int
    width: int
    height: int
    angle: float = 0.0
    unit: str = "pixel"
    paragraphs: List[Paragraph] = field(default_factory=list)
    lines: List[Line] = field(default_factory=list)
    words: List[Word] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "width": self.width,
            "height": self.height,
            "angle": self.angle,
            "unit": self.unit,
            "paragraphs": [p.to_dict() for p in self.paragraphs],
            "lines": [l.to_dict() for l in self.lines],
            "words": [w.to_dict() for w in self.words],
            "tables": [t.to_dict() for t in self.tables],
        }


@dataclass
class DocumentResult:
    """Complete document processing result."""

    document_type: DocumentType
    status: ProcessingStatus
    pages: List[DocumentPage] = field(default_factory=list)
    key_value_pairs: List[KeyValuePair] = field(default_factory=list)
    full_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "document_type": self.document_type.value,
            "status": self.status.value,
            "pages": [page.to_dict() for page in self.pages],
            "key_value_pairs": [kv.to_dict() for kv in self.key_value_pairs],
            "full_text": self.full_text,
            "metadata": self.metadata,
            "processing_time": self.processing_time,
        }
        if self.error_message:
            result["error_message"] = self.error_message
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "DocumentResult":
        """Create from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentResult":
        """Create from dictionary."""
        return cls(
            document_type=DocumentType(data.get("document_type", "image")),
            status=ProcessingStatus(data.get("status", "completed")),
            pages=[DocumentPage(**page) for page in data.get("pages", [])],
            key_value_pairs=[
                KeyValuePair(**kv) for kv in data.get("key_value_pairs", [])
            ],
            full_text=data.get("full_text", ""),
            metadata=data.get("metadata", {}),
            processing_time=data.get("processing_time", 0.0),
            error_message=data.get("error_message"),
        )


class DocumentRequest:
    """Request for document processing."""

    def __init__(
        self,
        document_path: str,
        document_type: DocumentType = DocumentType.IMAGE,
        options: Optional[Dict[str, Any]] = None,
    ):
        self.document_path = document_path
        self.document_type = document_type
        self.options = options or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_path": self.document_path,
            "document_type": self.document_type.value,
            "options": self.options,
        }
