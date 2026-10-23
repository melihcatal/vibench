from typing import List, Dict


class DocumentText:
    def __init__(self, text: str):
        self.text = text


class DocumentLayout:
    def __init__(self, layout: List[Dict]):
        self.layout = layout


class DocumentTables:
    def __init__(self, tables: List[Dict]):
        self.tables = tables


class DocumentKeyValues:
    def __init__(self, key_values: List[Dict]):
        self.key_values = key_values
