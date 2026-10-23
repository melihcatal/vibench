from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float


@dataclass
class OcrWord:
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None


@dataclass
class OcrLine:
    words: List[OcrWord]
    bounding_box: Optional[BoundingBox] = None

    @property
    def text(self) -> str:
        return " ".join(w.text for w in self.words)


@dataclass
class OcrBlock:
    block_type: str
    lines: List[OcrLine]
    bounding_box: Optional[BoundingBox] = None

    @property
    def text(self) -> str:
        return "\n".join(line.text for line in self.lines)


@dataclass
class TableCell:
    row_index: int
    col_index: int
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None


@dataclass
class TableStructure:
    cells: List[TableCell]
    num_rows: int
    num_columns: int
    bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None


@dataclass
class DocumentTextResult:
    raw_text: str
    lines: List[OcrLine]
    confidence: float
    page_count: int = 1


@dataclass
class DocumentLayoutResult:
    blocks: List[OcrBlock]
    tables: List[TableStructure]
    page_count: int = 1


@dataclass
class DocumentTableResult:
    tables: List[TableStructure]
    page_count: int = 1


@dataclass
class DocumentKeyValueResult:
    key_values: List[KeyValue]
    page_count: int = 1


def normalize_ocr_response(response_body: Any) -> DocumentTextResult:
    data = response_body.data if hasattr(response_body, "data") else response_body
    if isinstance(data, str):
        raw_text = data
        lines = [OcrLine(words=[OcrWord(text=data, confidence=1.0)])]
    elif isinstance(data, dict):
        raw_text = data.get("content", data.get("text", ""))
        lines = []
        for line_data in data.get("lines", []):
            words = [
                OcrWord(
                    text=w.get("text", ""),
                    confidence=w.get("confidence", 0.0),
                )
                for w in line_data.get("words", [])
            ]
            lines.append(OcrLine(words=words))
        if not lines and raw_text:
            lines = [OcrLine(words=[OcrWord(text=raw_text, confidence=1.0)])]
    else:
        raw_text = str(data)
        lines = [OcrLine(words=[OcrWord(text=raw_text, confidence=1.0)])]

    confidence = data.get("confidence", 1.0) if isinstance(data, dict) else 1.0
    page_count = data.get("page_count", 1) if isinstance(data, dict) else 1

    return DocumentTextResult(
        raw_text=raw_text,
        lines=lines,
        confidence=confidence,
        page_count=page_count,
    )


def normalize_layout_response(response_body: Any) -> DocumentLayoutResult:
    data = response_body.data if hasattr(response_body, "data") else response_body
    if isinstance(data, dict):
        blocks = []
        for block_data in data.get("blocks", []):
            lines = []
            for line_data in block_data.get("lines", []):
                words = [
                    OcrWord(
                        text=w.get("text", ""),
                        confidence=w.get("confidence", 0.0),
                    )
                    for w in line_data.get("words", [])
                ]
                lines.append(OcrLine(words=words))
            blocks.append(
                OcrBlock(
                    block_type=block_data.get("type", "unknown"),
                    lines=lines,
                )
            )
        tables = []
        for table_data in data.get("tables", []):
            cells = [
                TableCell(
                    row_index=c.get("row", 0),
                    col_index=c.get("column", 0),
                    text=c.get("text", ""),
                    confidence=c.get("confidence", 0.0),
                )
                for c in table_data.get("cells", [])
            ]
            tables.append(
                TableStructure(
                    cells=cells,
                    num_rows=table_data.get("num_rows", 0),
                    num_columns=table_data.get("num_columns", 0),
                )
            )
        page_count = data.get("page_count", 1)
    else:
        blocks = []
        tables = []
        page_count = 1

    return DocumentLayoutResult(blocks=blocks, tables=tables, page_count=page_count)


def normalize_table_response(response_body: Any) -> DocumentTableResult:
    data = response_body.data if hasattr(response_body, "data") else response_body
    if isinstance(data, dict):
        tables = []
        for table_data in data.get("tables", []):
            cells = [
                TableCell(
                    row_index=c.get("row", 0),
                    col_index=c.get("column", 0),
                    text=c.get("text", ""),
                    confidence=c.get("confidence", 0.0),
                )
                for c in table_data.get("cells", [])
            ]
            tables.append(
                TableStructure(
                    cells=cells,
                    num_rows=table_data.get("num_rows", 0),
                    num_columns=table_data.get("num_columns", 0),
                )
            )
        page_count = data.get("page_count", 1)
    else:
        tables = []
        page_count = 1

    return DocumentTableResult(tables=tables, page_count=page_count)


def normalize_key_value_response(response_body: Any) -> DocumentKeyValueResult:
    data = response_body.data if hasattr(response_body, "data") else response_body
    if isinstance(data, dict):
        key_values = []
        for kv_data in data.get("key_values", []):
            key_values.append(
                KeyValue(
                    key=kv_data.get("key", ""),
                    value=kv_data.get("value", ""),
                    confidence=kv_data.get("confidence", 0.0),
                )
            )
        page_count = data.get("page_count", 1)
    else:
        key_values = []
        page_count = 1

    return DocumentKeyValueResult(key_values=key_values, page_count=page_count)
