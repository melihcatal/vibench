from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass


@dataclass
class DocumentText:
    """Normalized document text output."""

    content: str
    language: Optional[str] = None


@dataclass
class DocumentLayout:
    """Normalized document layout output."""

    pages: List[Dict]
    lines: List[Dict]
    tables: List[Dict]
    figures: List[Dict]


@dataclass
class DocumentTable:
    """Normalized document table output."""

    row_count: int
    column_count: int
    cells: List[Dict]


@dataclass
class DocumentKeyValuePair:
    """Normalized key-value pair output."""

    key: str
    value: str
    confidence: float


class AnalyzeRequest(TypedDict):
    """Request structure for document analysis."""

    file_path: str
    model_id: str


class AnalyzeResponse(TypedDict):
    """Response structure for document analysis."""

    status: str
    data: Optional[Dict]


def normalize_text(text: str) -> DocumentText:
    """Normalize extracted text."""
    return DocumentText(content=text)


def normalize_layout(layout_data: Dict) -> DocumentLayout:
    """Normalize layout data."""
    return DocumentLayout(**layout_data)


def normalize_tables(tables: List[Dict]) -> List[DocumentTable]:
    """Normalize table data."""
    return [DocumentTable(**table) for table in tables]


def normalize_key_values(key_values: List[Dict]) -> List[DocumentKeyValuePair]:
    """Normalize key-value pairs."""
    return [DocumentKeyValuePair(**kv) for kv in key_values]
