from typing import List, Dict, Any

class ExtractedTextLine:
    def __init__(self, text: str, bounding_box: List[int]):
        self.text = text
        self.bounding_box = bounding_box

    def to_dict(self):
        return {"text": self.text, "bounding_box": self.bounding_box}

class ExtractedLayoutElement:
    def __init__(self, text: str, bounding_box: Dict[str, Any]):
        self.text = text
        self.bounding_box = bounding_box

    def to_dict(self):
        return {"text": self.text, "bounding_box": self.bounding_box}

class DocumentAnalysisResult:
    def __init__(self, text_lines: List[ExtractedTextLine] = None, layout_elements: List[ExtractedLayoutElement] = None, 
                 tables: List[Dict[str, Any]] = None, key_value_pairs: Dict[str, str] = None):
        self.text_lines = text_lines if text_lines is not None else []
        self.layout_elements = layout_elements if layout_elements is not None else []
        self.tables = tables if tables is not None else []
        self.key_value_pairs = key_value_pairs if key_value_pairs is not None else {}

    def to_dict(self):
        return {
            "text_lines": [line.to_dict() for line in self.text_lines],
            "layout_elements": [element.to_dict() for element in self.layout_elements],
            "tables": self.tables,
            "key_value_pairs": self.key_value_pairs
        }
