from typing import List, Dict, Any, Optional

class DocumentTextExtractionResponse:
    """Represents the response structure for text extraction.
    """
    def __init__(self, text: str, source_provider: str):
        self.text = text
        self.source_provider = source_provider

class DocumentLayoutBlock:
    """Represents a block of content in the document layout.
    """
    def __init__(self, block_type: str, text_content: str, bounding_box: List[float], confidence: float):
        self.block_type = block_type # e.g., "paragraph", "line", "word"
        self.text_content = text_content
        self.bounding_box = bounding_box # [x1, y1, x2, y2] normalized coordinates
        self.confidence = confidence

class DocumentLayoutResponse:
    """Represents the response structure for layout extraction.
    """
    def __init__(self, blocks: List[DocumentLayoutBlock], source_provider: str):
        self.blocks = blocks
        self.source_provider = source_provider

class DocumentTable:
    """Represents a table extracted from the document.
    """
    def __init__(self, rows: List[List[str]], bounding_box: List[float], confidence: float):
        self.rows = rows # List of lists, where each inner list is a row of cell texts
        self.bounding_box = bounding_box
        self.confidence = confidence

class DocumentTableResponse:
    """Represents the response structure for table extraction.
    """
    def __init__(self, tables: List[DocumentTable], source_provider: str):
        self.tables = tables
        self.source_provider = source_provider

class KeyValuePair:
    """Represents a key-value pair extracted from the document.
    """
    def __init__(self, key: str, value: str, key_bounding_box: List[float], value_bounding_box: List[float], confidence: float):
        self.key = key
        self.value = value
        self.key_bounding_box = key_bounding_box
        self.value_bounding_box = value_bounding_box
        self.confidence = confidence

class DocumentKeyValueResponse:
    """Represents the response structure for key-value pair extraction.
    """
    def __init__(self, key_value_pairs: List[KeyValuePair], source_provider: str):
        self.key_value_pairs = key_value_pairs
        self.source_provider = source_provider
