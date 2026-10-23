from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    image_bytes: bytes
    language_code: str = 'en'


@dataclass
class LayoutRequest:
    image_bytes: bytes


@dataclass
class TableRequest:
    image_bytes: bytes


@dataclass
class KeyValueRequest:
    image_bytes: bytes


@dataclass
class NormalizedResult:
    text: str
    blocks: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    key_values: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _page_to_blocks(page: Any) -> List[Dict[str, Any]]:
    blocks = []
    for paragraph in getattr(page, 'paragraphs', []):
        blocks.append({'type': 'paragraph', 'text': _text_from_layout(paragraph.layout)})
    for token in getattr(page, 'tokens', []):
        blocks.append({'type': 'token', 'text': _text_from_layout(token.layout)})
    return blocks


def _text_from_layout(layout: Any) -> str:
    return getattr(layout, 'text_anchor', None).content if getattr(layout, 'text_anchor', None) else ''


def normalize_ocr_result(document: Any) -> NormalizedResult:
    pages = getattr(document, 'pages', [])
    text = getattr(document, 'text', '')
    blocks = []
    for page in pages:
        blocks.extend(_page_to_blocks(page))
    return NormalizedResult(text=text, blocks=blocks, tables=[], key_values=[])


def normalize_layout_result(document: Any) -> NormalizedResult:
    blocks = []
    for page in getattr(document, 'pages', []):
        for block in getattr(page, 'blocks', []):
            blocks.append({'type': 'block', 'text': _text_from_layout(block.layout)})
        for line in getattr(page, 'lines', []):
            blocks.append({'type': 'line', 'text': _text_from_layout(line.layout)})
    return NormalizedResult(text=getattr(document, 'text', ''), blocks=blocks, tables=[], key_values=[])


def normalize_table_result(document: Any) -> NormalizedResult:
    tables = []
    for page in getattr(document, 'pages', []):
        for table in getattr(page, 'tables', []):
            tables.append({'header_rows': len(getattr(table, 'header_rows', [])), 'body_rows': len(getattr(table, 'body_rows', []))})
    return NormalizedResult(text=getattr(document, 'text', ''), blocks=[], tables=tables, key_values=[])


def normalize_key_value_result(document: Any) -> NormalizedResult:
    key_values = []
    for page in getattr(document, 'pages', []):
        for pair in getattr(page, 'form_fields', []):
            key_values.append({'key': _text_from_layout(pair.field_name), 'value': _text_from_layout(pair.field_value)})
    return NormalizedResult(text=getattr(document, 'text', ''), blocks=[], tables=[], key_values=key_values)
