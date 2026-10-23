from typing import Dict, Any, Optional

class DocumentPayload:
    def __init__(self, document_bytes: bytes, content_type: Optional[str] = None):
        self.document_bytes = document_bytes
        self.content_type = content_type

class ExtractedTextResponse:
    def __init__(self, text: str):
        self.text = text

class LayoutElement:
    def __init__(self, block_type: str, text: Optional[str] = None, bounding_box: Optional[Dict] = None):
        self.block_type = block_type
        self.text = text
        self.bounding_box = bounding_box

class ExtractedLayoutResponse:
    def __init__(self, layout_elements: list[LayoutElement]):
        self.layout_elements = layout_elements

class TableCell:
    def __init__(self, text: str, row_index: int, column_index: int, row_span: int, column_span: int):
        self.text = text
        self.row_index = row_index
        self.column_index = column_index
        self.row_span = row_span
        self.column_span = column_span

class ExtractedTable:
    def __init__(self, table_id: str, cells: list[TableCell]):
        self.table_id = table_id
        self.cells = cells

class ExtractedTablesResponse:
    def __init__(self, tables: list[ExtractedTable]):
        self.tables = tables

class KeyValueEntry:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

class ExtractedKeyValuesResponse:
    def __init__(self, key_values: list[KeyValueEntry]):
        self.key_values = key_values
