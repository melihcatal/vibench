
from dataclasses import dataclass
from typing import Optional, List, Any

@dataclass
class DocumentFile:
    """Represents a document to be processed."""
    file_path: Optional[str] = None
    file_bytes: Optional[bytes] = None
    file_url: Optional[str] = None

@dataclass
class ExtractedText:
    """Represents the plain text extracted from a document."""
    content: str
    raw_response: Any

@dataclass
class ExtractedLayout:
    """Represents layout elements extracted from a document."""
    pages: List[Any]
    paragraphs: List[Any]
    raw_response: Any
    
@dataclass
class ExtractedTable:
    """Represents a single table extracted from a document."""
    row_count: int
    column_count: int
    cells: List[Any]

@dataclass
class ExtractedTables:
    """Represents a collection of tables extracted from a document."""
    tables: List[ExtractedTable]
    raw_response: Any

@dataclass
class ExtractedKeyValuePair:
    """Represents a single key-value pair."""
    key: str
    value: Optional[str]
    confidence: float

@dataclass
class ExtractedKeyValues:
    """Represents a collection of key-value pairs."""
    pairs: List[ExtractedKeyValuePair]
    raw_response: Any
