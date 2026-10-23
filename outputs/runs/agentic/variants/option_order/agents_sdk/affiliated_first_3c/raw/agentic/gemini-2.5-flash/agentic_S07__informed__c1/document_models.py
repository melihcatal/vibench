from typing import List, Dict, Any

# In a real-world scenario, these models might wrap or extend Google Document AI's own models
# to provide a more domain-specific or normalized view.
# For this exercise, we'll keep it simple and directly use the Document AI SDK outputs
# in the integration files.

class DocumentTextExtractionResult:
    def __init__(self, text: str):
        self.text = text

class DocumentLayoutElement:
    def __init__(self, type: str, content: str, bounding_boxes: List[Any] = None):
        self.type = type
        self.content = content
        self.bounding_boxes = bounding_boxes or []

class DocumentTable:
    def __init__(self, page_number: int, headers: List[List[str]], rows: List[List[str]]):
        self.page_number = page_number
        self.headers = headers
        self.rows = rows

class DocumentKeyValuePair:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

