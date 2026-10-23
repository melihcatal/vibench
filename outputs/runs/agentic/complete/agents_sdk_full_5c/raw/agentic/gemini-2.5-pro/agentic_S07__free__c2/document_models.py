
from typing import List, NamedTuple, Optional

class ExtractedText(NamedTuple):
    """Represents the plain text content extracted from a document."""
    content: str

class LayoutElement(NamedTuple):
    """Represents a block or paragraph of text with its bounding region."""
    content: str
    bounding_box: List[float]
    role: Optional[str] = None

class TableCell(NamedTuple):
    """Represents a single cell within a table."""
    content: str
    row_index: int
    column_index: int
    kind: Optional[str] = 'content' # e.g., 'content', 'rowHeader', 'columnHeader'

class ExtractedTable(NamedTuple):
    """Represents a full table with its cells and structure."""
    cells: List[TableCell]
    row_count: int
    column_count: int
    bounding_box: List[float]

class KeyValuePair(NamedTuple):
    """Represents an extracted key-value pair from a form."""
    key: str
    value: Optional[str]
    confidence: float
