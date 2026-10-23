from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    content: Any
    content_type: str = "application/octet-stream"
    model_id: Optional[str] = None


@dataclass
class NormalizedBlock:
    text: str
    kind: str
    confidence: float = 0.0
    row_index: Optional[int] = None
    column_index: Optional[int] = None


@dataclass
class DocumentResponse:
    text: str = ""
    blocks: List[NormalizedBlock] = field(default_factory=list)
    key_values: Dict[str, str] = field(default_factory=dict)
    tables: List[List[List[str]]] = field(default_factory=list)
    raw: Any = None


def normalize_analyze_result(result: Any) -> DocumentResponse:
    text = getattr(result, "content", "") or ""
    blocks = []
    key_values = {}
    tables = []
    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            blocks.append(
                NormalizedBlock(
                    text=getattr(line, "content", ""),
                    kind="line",
                    confidence=getattr(line, "confidence", 0.0) or 0.0,
                )
            )
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", "") or ""
        value = getattr(getattr(kv, "value", None), "content", "") or ""
        if key:
            key_values[key] = value
    for table in getattr(result, "tables", []) or []:
        rows = []
        for row in getattr(table, "cells", []) or []:
            rows.append([getattr(row, "content", "")])
        if rows:
            tables.append(rows)
    return DocumentResponse(
        text=text, blocks=blocks, key_values=key_values, tables=tables, raw=result
    )
