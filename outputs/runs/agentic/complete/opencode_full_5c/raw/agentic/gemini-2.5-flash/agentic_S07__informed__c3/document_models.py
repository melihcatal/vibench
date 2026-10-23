from typing import List, Dict, Any


class ExtractedText:
    def __init__(self, content: str):
        self.content = content


class ExtractedLayout:
    def __init__(self, pages: List[Dict[str, Any]]):
        self.pages = pages


class ExtractedTables:
    def __init__(self, tables: List[Dict[str, Any]]):
        self.tables = tables


class ExtractedKeyValues:
    def __init__(self, key_value_pairs: List[Dict[str, Any]]):
        self.key_value_pairs = key_value_pairs
