from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class DocumentRequest:
    content: Optional[bytes] = None
    base64_content: Optional[str] = None
    source_path: Optional[str] = None

    @classmethod
    def from_input(cls, source: Union[str, bytes, bytearray, "DocumentRequest", Path]) -> "DocumentRequest":
        if isinstance(source, cls):
            return source
        if isinstance(source, (bytes, bytearray)):
            return cls(content=bytes(source))
        if isinstance(source, Path):
            return cls(source_path=str(source))
        if isinstance(source, str):
            if Path(source).exists():
                return cls(source_path=source)
            return cls(base64_content=source)
        raise TypeError("Unsupported document input")


@dataclass
class TextExtractionResult:
    text: str
    raw: Dict[str, Any]


@dataclass
class LayoutBlock:
    block_type: str
    text: Optional[str] = None
    confidence: Optional[float] = None
    geometry: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


@dataclass
class LayoutExtractionResult:
    blocks: List[LayoutBlock]
    raw: Dict[str, Any]


@dataclass
class TableCell:
    row_index: Optional[int]
    column_index: Optional[int]
    text: Optional[str]
    confidence: Optional[float]
    id: Optional[str] = None


@dataclass
class Table:
    cells: List[TableCell]
    id: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class TableExtractionResult:
    tables: List[Table]
    raw: Dict[str, Any]


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    id: Optional[str] = None


@dataclass
class KeyValueExtractionResult:
    key_values: List[KeyValuePair]
    raw: Dict[str, Any]
