from typing import Any, Dict, List
from azure.ai.documentintelligence.models import AnalyzeResult


def normalize_text(result: AnalyzeResult) -> str:
    return result.content or ""


def normalize_layout(result: AnalyzeResult) -> List[Dict[str, Any]]:
    elements = []
    for page in result.pages or []:
        for paragraph in page.paragraphs or []:
            bbox = []
            if (
                paragraph.bounding_regions
                and len(paragraph.bounding_regions) > 0
                and paragraph.bounding_regions[0].polygon
            ):
                bbox = [
                    {"x": p.x, "y": p.y} for p in paragraph.bounding_regions[0].polygon
                ]
            elements.append(
                {
                    "type": "paragraph",
                    "text": paragraph.content or "",
                    "bounding_box": bbox,
                }
            )
    return elements


def normalize_tables(result: AnalyzeResult) -> List[List[str]]:
    tables = []
    for page in result.pages or []:
        for table in page.tables or []:
            if table.row_count is None or table.column_count is None:
                continue
            grid = [
                ["" for _ in range(table.column_count)] for _ in range(table.row_count)
            ]
            for cell in table.cells or []:
                row_idx = getattr(cell, "row_index", None)
                col_idx = getattr(cell, "column_index", None)
                if row_idx is not None and col_idx is not None:
                    grid[row_idx][col_idx] = cell.content or ""
            tables.append(grid)
    return tables


def normalize_key_values(result: AnalyzeResult) -> List[Dict[str, Any]]:
    kvs = []
    for kv_pair in result.key_value_pairs or []:
        key_text = kv_pair.key.content if kv_pair.key else ""
        value_text = kv_pair.value.content if kv_pair.value else ""
        conf = getattr(kv_pair, "confidence", 0.0)
        kvs.append({"key": key_text, "value": value_text, "confidence": conf})
    return kvs
