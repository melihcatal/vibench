from typing import List, Dict, Any, Optional

class ExtractedText:
    def __init__(self, text: str):
        self.text = text

class BoundingRegion:
    def __init__(self, page_number: int, polygon: List[float]):
        self.page_number = page_number
        self.polygon = polygon

class LayoutBlock:
    def __init__(self, content: str, kind: str, bounding_regions: List[BoundingRegion]):
        self.content = content
        self.kind = kind
        self.bounding_regions = bounding_regions

class ExtractedLayout:
    def __init__(self, blocks: List[LayoutBlock]):
        self.blocks = blocks

class TableCell:
    def __init__(
        self, 
        content: str,
        row_index: int,
        column_index: int,
        row_span: int = 1,
        column_span: int = 1,
        kind: Optional[str] = None
    ):
        self.content = content
        self.row_index = row_index
        self.column_index = column_index
        self.row_span = row_span
        self.column_span = column_span
        self.kind = kind

class ExtractedTable:
    def __init__(
        self, 
        row_count: int,
        column_count: int,
        cells: List[TableCell],
        bounding_regions: List[BoundingRegion]
    ):
        self.row_count = row_count
        self.column_count = column_count
        self.cells = cells
        self.bounding_regions = bounding_regions

class KeyValuePair:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

class ExtractedKeyValuePair:
    def __init__(self, key_value_pairs: List[KeyValuePair]):
        self.key_value_pairs = key_value_pairs

class TranslationResponse:
    def __init__(self, translated_text: str, detected_language_code: Optional[str] = None):
        self.translated_text = translated_text
        self.detected_language_code = detected_language_code

class SafetyCategoryResult:
    def __init__(self, category: str, severity: int, flagged: bool):
        self.category = category
        self.severity = severity
        self.flagged = flagged

class SafetyResponse:
    def __init__(self, flagged: bool, categories: List[SafetyCategoryResult]):
        self.flagged = flagged
        self.categories = categories

class ExtractedFields:
    def __init__(self, fields: Dict[str, Any]):
        self.fields = fields

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
