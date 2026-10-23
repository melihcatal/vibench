from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class OcrLine:
    text: str
    confidence: float
    bounding_box: Optional[List[float]] = None


@dataclass
class OcrPage:
    text: str
    lines: List[OcrLine] = field(default_factory=list)
    width: Optional[float] = None
    height: Optional[float] = None
    unit: Optional[str] = None


@dataclass
class OcrResult:
    pages: List[OcrPage] = field(default_factory=list)
    model_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None

    def get_full_text(self) -> str:
        return "\n".join(page.text for page in self.pages)

    def get_all_lines(self) -> List[OcrLine]:
        lines = []
        for page in self.pages:
            lines.extend(page.lines)
        return lines


@dataclass
class LayoutBlock:
    kind: str
    text: str
    confidence: float
    bounding_box: Optional[List[float]] = None
    spans: Optional[List[Dict[str, int]]] = None


@dataclass
class LayoutTable:
    row_count: int
    column_count: int
    cells: List[Dict[str, Any]] = field(default_factory=list)
    bounding_box: Optional[List[float]] = None
    confidence: float = 0.0


@dataclass
class LayoutResult:
    pages: List[OcrPage] = field(default_factory=list)
    blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[LayoutTable] = field(default_factory=list)
    model_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None

    def get_full_text(self) -> str:
        return "\n".join(page.text for page in self.pages)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    confidence: float = 0.0


@dataclass
class TableRow:
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class TableResult:
    tables: List[List[TableRow]] = field(default_factory=list)
    table_count: int = 0
    model_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None

    def get_table_as_csv(self, table_index: int = 0) -> str:
        if not self.tables or table_index >= len(self.tables):
            return ""
        rows = self.tables[table_index]
        csv_lines = []
        for row in rows:
            csv_lines.append(",".join(cell.text for cell in row.cells))
        return "\n".join(csv_lines)


@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float = 0.0
    key_bounding_box: Optional[List[float]] = None
    value_bounding_box: Optional[List[float]] = None


@dataclass
class KeyValueResult:
    key_values: List[KeyValue] = field(default_factory=list)
    model_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, str]:
        return {kv.key: kv.value for kv in self.key_values}


def normalize_ocr_response(azure_result) -> OcrResult:
    pages = []
    for page in azure_result.pages:
        lines = []
        for line in page.lines:
            lines.append(
                OcrLine(
                    text=line.content,
                    confidence=getattr(line, "confidence", 1.0),
                    bounding_box=getattr(line, "bounding_regions", None),
                )
            )
        pages.append(
            OcrPage(
                text=page.content
                if hasattr(page, "content")
                else "\n".join(l.text for l in lines),
                lines=lines,
                width=getattr(page, "width", None),
                height=getattr(page, "height", None),
                unit=getattr(page, "unit", None),
            )
        )
    return OcrResult(
        pages=pages,
        model_id=azure_result.model_id,
        raw_response=azure_result.as_dict()
        if hasattr(azure_result, "as_dict")
        else None,
    )


def normalize_layout_response(azure_result) -> LayoutResult:
    pages = []
    for page in azure_result.pages:
        lines = []
        for line in page.lines:
            lines.append(
                OcrLine(
                    text=line.content,
                    confidence=getattr(line, "confidence", 1.0),
                    bounding_box=getattr(line, "bounding_regions", None),
                )
            )
        pages.append(
            OcrPage(
                text=page.content
                if hasattr(page, "content")
                else "\n".join(l.text for l in lines),
                lines=lines,
                width=getattr(page, "width", None),
                height=getattr(page, "height", None),
                unit=getattr(page, "unit", None),
            )
        )

    blocks = []
    for paragraph in getattr(azure_result, "paragraphs", []):
        blocks.append(
            LayoutBlock(
                kind=getattr(paragraph, "role", "paragraph"),
                text=paragraph.content,
                confidence=getattr(paragraph, "confidence", 1.0),
                bounding_box=getattr(paragraph, "bounding_regions", None),
                spans=getattr(paragraph, "spans", None),
            )
        )

    tables = []
    for table in getattr(azure_result, "tables", []):
        cells = []
        for cell in table.cells:
            cells.append(
                {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "text": cell.content,
                    "row_span": cell.row_span,
                    "column_span": cell.column_span,
                    "confidence": getattr(cell, "confidence", 1.0),
                }
            )
        tables.append(
            LayoutTable(
                row_count=table.row_count,
                column_count=table.column_count,
                cells=cells,
                bounding_box=getattr(table, "bounding_regions", None),
                confidence=getattr(table, "confidence", 1.0),
            )
        )

    return LayoutResult(
        pages=pages,
        blocks=blocks,
        tables=tables,
        model_id=azure_result.model_id,
        raw_response=azure_result.as_dict()
        if hasattr(azure_result, "as_dict")
        else None,
    )


def normalize_table_response(azure_result) -> TableResult:
    all_tables = []
    for table in getattr(azure_result, "tables", []):
        rows_dict = {}
        for cell in table.cells:
            row_idx = cell.row_index
            if row_idx not in rows_dict:
                rows_dict[row_idx] = []
            rows_dict[row_idx].append(
                TableCell(
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    text=cell.content,
                    row_span=cell.row_span,
                    column_span=cell.column_span,
                    confidence=getattr(cell, "confidence", 1.0),
                )
            )

        row_list = []
        for idx in sorted(rows_dict.keys()):
            row_list.append(
                TableRow(cells=sorted(rows_dict[idx], key=lambda c: c.column_index))
            )
        all_tables.append(row_list)

    return TableResult(
        tables=all_tables,
        table_count=len(all_tables),
        model_id=azure_result.model_id,
        raw_response=azure_result.as_dict()
        if hasattr(azure_result, "as_dict")
        else None,
    )


def normalize_kv_response(azure_result) -> KeyValueResult:
    key_values = []
    for kv in getattr(azure_result, "key_value_pairs", []):
        key_text = kv.key.content if kv.key else ""
        value_text = kv.value.content if kv.value else ""
        key_values.append(
            KeyValue(
                key=key_text,
                value=value_text,
                confidence=getattr(kv, "confidence", 1.0),
                key_bounding_box=getattr(kv.key, "bounding_regions", None)
                if kv.key
                else None,
                value_bounding_box=getattr(kv.value, "bounding_regions", None)
                if kv.value
                else None,
            )
        )
    return KeyValueResult(
        key_values=key_values,
        model_id=azure_result.model_id,
        raw_response=azure_result.as_dict()
        if hasattr(azure_result, "as_dict")
        else None,
    )
