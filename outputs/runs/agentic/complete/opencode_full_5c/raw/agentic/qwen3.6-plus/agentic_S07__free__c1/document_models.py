from __future__ import annotations

import base64
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class DocumentSource(str, Enum):
    FILE_PATH = "file_path"
    BASE64 = "base64"
    URL = "url"


@dataclass
class DocumentRequest:
    source_type: DocumentSource
    file_path: Optional[str] = None
    base64_content: Optional[str] = None
    url: Optional[str] = None
    content_type: str = "application/pdf"

    @classmethod
    def from_file(
        cls, file_path: str, content_type: str = "application/pdf"
    ) -> DocumentRequest:
        return cls(
            source_type=DocumentSource.FILE_PATH,
            file_path=file_path,
            content_type=content_type,
        )

    @classmethod
    def from_base64(
        cls, base64_content: str, content_type: str = "application/pdf"
    ) -> DocumentRequest:
        return cls(
            source_type=DocumentSource.BASE64,
            base64_content=base64_content,
            content_type=content_type,
        )

    @classmethod
    def from_url(cls, url: str) -> DocumentRequest:
        return cls(
            source_type=DocumentSource.URL,
            url=url,
        )

    def read_bytes(self) -> bytes:
        if self.source_type == DocumentSource.FILE_PATH and self.file_path:
            return Path(self.file_path).read_bytes()
        if self.source_type == DocumentSource.BASE64 and self.base64_content:
            return base64.b64decode(self.base64_content)
        raise ValueError("Cannot read bytes from URL source")


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float


@dataclass
class OcrLine:
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    words: list[dict] = field(default_factory=list)


@dataclass
class OcrResult:
    text: str
    lines: list[OcrLine] = field(default_factory=list)
    confidence: float = 0.0
    page_number: int = 1
    language: str = "en"


@dataclass
class LayoutBlock:
    block_type: str
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    role: Optional[str] = None


@dataclass
class LayoutResult:
    blocks: list[LayoutBlock] = field(default_factory=list)
    page_number: int = 1
    width: float = 0.0
    height: float = 0.0


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    confidence: float
    is_header: bool = False
    row_span: int = 1
    column_span: int = 1
    bounding_box: Optional[BoundingBox] = None


@dataclass
class TableResult:
    cells: list[TableCell] = field(default_factory=list)
    row_count: int = 0
    column_count: int = 0
    page_number: int = 1
    bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValueResult:
    pairs: list[KeyValuePair] = field(default_factory=list)
    page_number: int = 1


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class FieldExtractionResult:
    fields: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    raw_response: Optional[dict] = None


@dataclass
class EmbeddingResult:
    embeddings: list[list[float]] = field(default_factory=list)
    section_texts: list[str] = field(default_factory=list)
    model: str = ""
    total_tokens: int = 0


def normalize_confidence(raw_value: Optional[float], default: float = 0.0) -> float:
    if raw_value is None:
        return default
    return max(0.0, min(1.0, raw_value))


def normalize_bounding_box(polygon: Optional[list[float]]) -> Optional[BoundingBox]:
    if not polygon or len(polygon) < 8:
        return None
    xs = [polygon[i] for i in range(0, len(polygon), 2)]
    ys = [polygon[i] for i in range(1, len(polygon), 2)]
    return BoundingBox(
        x=min(xs),
        y=min(ys),
        width=max(xs) - min(xs),
        height=max(ys) - min(ys),
    )


def split_text_into_sections(text: str, max_section_length: int = 1000) -> list[str]:
    if not text:
        return []
    paragraphs = text.split("\n\n")
    sections: list[str] = []
    current_section = ""
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(current_section) + len(paragraph) + 2 > max_section_length:
            if current_section:
                sections.append(current_section.strip())
            current_section = paragraph
        else:
            if current_section:
                current_section += "\n\n" + paragraph
            else:
                current_section = paragraph
    if current_section:
        sections.append(current_section.strip())
    return sections
