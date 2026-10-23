from typing import List, Dict, Any

class DocumentInput:
    """Represents the input for document processing tasks."""
    def __init__(self, image_path: str, mime_type: str = "application/octet-stream", features: List[str] = None):
        self.image_path = image_path
        self.mime_type = mime_type
        self.features = features if features is not None else []

class ExtractedText:
    """Represents extracted plain text from a document."""
    def __init__(self, text_content: str):
        self.text_content = text_content

class ExtractedLayout:
    """Represents extracted layout elements (blocks, lines, etc.)."""
    def __init__(self, layout_data: List[Dict[str, Any]]):
        self.layout_data = layout_data

class ExtractedTable:
    """Represents extracted table data with cells and structure."""
    def __init__(self, table_data: List[Dict[str, Any]]):
        self.table_data = table_data

class ExtractedKeyValuePairs:
    """Represents extracted key-value pairs from a form-like document."""
    def __init__(self, key_value_pairs: Dict[str, str]):
        self.key_value_pairs = key_value_pairs
