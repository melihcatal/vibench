from typing import List, Dict, Any

class ExtractedText:
    """Represents extracted plain text."""
    def __init__(self, text: str):
        self.text = text

class ExtractedLayoutElement:
    """Represents a generic extracted layout element."""
    def __init__(self, bounding_box: List[float], text_content: str, type: str):
        self.bounding_box = bounding_box
        self.text_content = text_content
        self.type = type # e.g., 'paragraph', 'line', 'block'

class ExtractedTable:
    """Represents an extracted table with rows and cells."""
    def __init__(self, header_rows: List[List[str]], body_rows: List[List[str]]):
        self.header_rows = header_rows
        self.body_rows = body_rows

class ExtractedKeyValuePair:
    """Represents an extracted key-value pair from a form."""
    def __init__(self, key: str, value: str, key_bounding_box: List[float], value_bounding_box: List[float]):
        self.key = key
        self.value = value
        self.key_bounding_box = key_bounding_box
        self.value_bounding_box = value_bounding_box

# Helper for converting Document AI bounding poly to a simpler list of floats
def normalize_bounding_poly(bounding_poly) -> List[float]:
    if not bounding_poly or not bounding_poly.vertices:
        return []
    # Assuming the first vertex is top-left and last is bottom-right for a simple representation
    # This is a simplification; a real implementation might process all vertices
    return [
        bounding_poly.vertices[0].x, bounding_poly.vertices[0].y,
        bounding_poly.vertices[-1].x, bounding_poly.vertices[-1].y
    ]
