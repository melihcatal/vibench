from typing import List, Dict, Any
from azure.ai.documentintelligence.models import AnalyzeResult

OCRText = str
OCRLayout = List[Dict[str, Any]]
OCRTable = List[List[str]]
OCRKeyValues = Dict[str, str]


def get_ocr_text(result: AnalyzeResult) -> OCRText:
    text = ""
    for page in result.pages or []:
        for line in page.lines or []:
            text += line.content + "\n"
    return text.strip()


def get_ocr_layout(result: AnalyzeResult) -> OCRLayout:
    elements: OCRLayout = []
    for page in result.pages or []:
        for line in page.lines or []:
            elements.append(
                {
                    "type": "line",
                    "content": line.content,
                    "confidence": getattr(line, "confidence", 0.0),
                    "page": page.page_number,
                }
            )
    for table_idx, table in enumerate(result.tables or []):
        elements.append(
            {
                "type": "table",
                "table_index": table_idx,
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": [
                    {
                        "row": c.row_index,
                        "col": c.column_index,
                        "content": c.content or "",
                    }
                    for c in table.cells
                ],
            }
        )
    return elements


def get_ocr_tables(result: AnalyzeResult) -> List[OCRTable]:
    tables: List[OCRTable] = []
    for table in result.tables or []:
        grid: OCRTable = [
            ["" for _ in range(table.column_count)] for _ in range(table.row_count)
        ]
        for cell in table.cells:
            grid[cell.row_index][cell.column_index] = cell.content or ""
        tables.append(grid)
    return tables


def get_ocr_key_values(result: AnalyzeResult) -> OCRKeyValues:
    kv: OCRKeyValues = {}
    for kvp in getattr(result, "key_value_pairs", []):
        key = kvp.key.content if kvp.key else None
        val = kvp.value.content if kvp.value else None
        if key and val:
            kv[key.strip(":?")] = val
    return kv


def parse_invoice_fields(result: AnalyzeResult) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}
    if result.documents:
        doc = result.documents[0]
        for fname, field in doc.fields.items():
            if field.content:
                fields[fname] = field.content
            elif field.value_string:
                fields[fname] = field.value_string
            elif field.value_number:
                fields[fname] = field.value_number
            elif field.value_array:
                fields[fname] = [v.value_string for v in field.value_array]
            else:
                fields[fname] = None
    return fields
