
from typing import List, Dict, Any

class ExtractedText:
    def __init__(self, text: str):
        self.text = text

class ExtractedLayout:
    def __init__(self, paragraphs: List[Dict[str, Any]], tables: List[Dict[str, Any]], key_values: List[Dict[str, Any]]):
        self.paragraphs = paragraphs
        self.tables = tables
        self.key_values = key_values

class ExtractedTable:
    def __init__(self, cells: List[Dict[str, Any]], rows: int, columns: int):
        self.cells = cells
        self.rows = rows
        self.columns = columns

class ExtractedKeyValue:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
