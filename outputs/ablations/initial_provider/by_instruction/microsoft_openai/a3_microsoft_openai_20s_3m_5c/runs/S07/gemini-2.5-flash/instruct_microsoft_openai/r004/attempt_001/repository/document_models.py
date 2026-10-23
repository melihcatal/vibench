from typing import List, Dict, Any

class ExtractedText:
    def __init__(self, text: str, page_number: int = None):
        self.text = text
        self.page_number = page_number

    def to_dict(self):
        return {"text": self.text, "page_number": self.page_number}

class ExtractedLayout:
    def __init__(self, blocks: List[Dict[str, Any]], page_number: int = None):
        self.blocks = blocks
        self.page_number = page_number

    def to_dict(self):
        return {"blocks": self.blocks, "page_number": self.page_number}

class ExtractedTable:
    def __init__(self, cells: List[Dict[str, Any]], row_count: int, column_count: int, page_number: int = None):
        self.cells = cells
        self.row_count = row_count
        self.column_count = column_count
        self.page_number = page_number

    def to_dict(self):
        return {
            "cells": self.cells,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "page_number": self.page_number
        }

class ExtractedKeyValue:
    def __init__(self, key: str, value: str, page_number: int = None):
        self.key = key
        self.value = value
        self.page_number = page_number

    def to_dict(self):
        return {"key": self.key, "value": self.value, "page_number": self.page_number}
