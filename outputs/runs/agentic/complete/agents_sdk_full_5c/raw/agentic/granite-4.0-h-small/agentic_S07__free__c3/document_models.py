import os
from typing import List
from document_models import LayoutBlock

class TableSpec(TypedDict):
    column_headers: List[str]
    rows: List[List[str]]

class KeyValueSpec(TypedDict):
    key: str
    value: str

# Helper utilities for later-step services
class DocumentFieldExtractor:
    @staticmethod
def extract_tables(blocks: List[LayoutBlock]) -> List[TableSpec]:
        # Placeholder - integrate with a table extraction model
        return []

    @staticmethod
def extract_key_values(blocks: List[LayoutBlock]) -> List[KeyValueSpec]:
        # Placeholder - integrate with form key-value model
        return []
