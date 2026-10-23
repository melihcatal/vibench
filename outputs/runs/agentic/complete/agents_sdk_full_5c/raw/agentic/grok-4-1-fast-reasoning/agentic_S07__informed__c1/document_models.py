from typing import Any, Dict, List, Optional
from azure.ai.documentintelligence.models import AnalyzeResult

def normalize_text(result: AnalyzeResult) -> str:
    return result.content or ""

def normalize_layout(result: AnalyzeResult) -> List[Dict[str, Any]]:
    layout = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    bbox = line.bounding_regions[0].polygon if line.bounding_regions else []
                    layout.append({
                        "type": "line",
                        "content": line.content,
                        "bounding_box": bbox,
                        "confidence": getattr(line, "confidence", 0.0),
                    })
    return layout

def normalize_tables(result: AnalyzeResult) -> List[Dict[str, Any]]:
    tables = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                cells.append({
                    "content": cell.content,
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "confidence": getattr(cell, "confidence", 0.0),
                })
            tables.append({
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": cells,
            })
    return tables

def normalize_key_values(result: AnalyzeResult) -> List[Dict[str, str]]:
    kvps = []
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            key_content = kvp.key.content if kvp.key else None
            value_content = kvp.value.content if kvp.value else ""
            if key_content:
                kvps.append({
                    "key": key_content,
                    "value": value_content,
                    "confidence": getattr(kvp, "confidence", 0.0),
                })
    return kvps