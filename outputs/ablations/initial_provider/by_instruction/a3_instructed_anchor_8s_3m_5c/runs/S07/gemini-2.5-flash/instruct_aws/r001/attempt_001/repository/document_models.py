from typing import List, Dict, Any

# Basic models for extracted content - can be expanded as needed

class ExtractedText:
    def __init__(self, text: str, block_type: str = "LINE", confidence: float = None):
        self.text = text
        self.block_type = block_type
        self.confidence = confidence

    def to_dict(self):
        return {"text": self.text, "block_type": self.block_type, "confidence": self.confidence}

class ExtractedLayoutElement:
    def __init__(self, element_type: str, text: str = None, geometry: Dict = None, confidence: float = None):
        self.element_type = element_type # e.g., TITLE, PARAGRAPH, LIST, TABLE, FIGURE
        self.text = text
        self.geometry = geometry
        self.confidence = confidence

    def to_dict(self):
        return {"element_type": self.element_type, "text": self.text, "geometry": self.geometry, "confidence": self.confidence}

class ExtractedTableCell:
    def __init__(self, text: str, row_index: int, column_index: int, row_span: int = 1, column_span: int = 1, confidence: float = None):
        self.text = text
        self.row_index = row_index
        self.column_index = column_index
        self.row_span = row_span
        self.column_span = column_span
        self.confidence = confidence

    def to_dict(self):
        return {"text": self.text, "row_index": self.row_index, "column_index": self.column_index, "row_span": self.row_span, "column_span": self.column_span, "confidence": self.confidence}

class ExtractedTable:
    def __init__(self, cells: List[ExtractedTableCell], geometry: Dict = None, confidence: float = None):
        self.cells = cells
        self.geometry = geometry
        self.confidence = confidence

    def to_dict(self):
        return {"cells": [cell.to_dict() for cell in self.cells], "geometry": self.geometry, "confidence": self.confidence}

class ExtractedKeyValuePair:
    def __init__(self, key: str, value: str, key_geometry: Dict = None, value_geometry: Dict = None, confidence: float = None):
        self.key = key
        self.value = value
        self.key_geometry = key_geometry
        self.value_geometry = value_geometry
        self.confidence = confidence

    def to_dict(self):
        return {"key": self.key, "value": self.value, "key_geometry": self.key_geometry, "value_geometry": self.value_geometry, "confidence": self.confidence}
