from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentInput:
    content: bytes
    content_type: Optional[str] = None
    filename: Optional[str] = None


@dataclass
class NormalizedText:
    text: str
    language: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class NormalizedDocumentResult:
    raw: Any
    data: Dict[str, Any]


def build_image_source(document: DocumentInput) -> bytes:
    if not document.content:
        raise ValueError("document content cannot be empty")
    return document.content


def normalize_text_result(result: Any) -> NormalizedText:
    text = getattr(result, "content", None) or getattr(result, "text", None) or ""
    language = getattr(result, "language", None)
    confidence = getattr(result, "confidence", None)
    return NormalizedText(text=text, language=language, confidence=confidence)


def normalize_layout_result(result: Any) -> NormalizedDocumentResult:
    return NormalizedDocumentResult(raw=result, data={
        "paragraphs": [getattr(p, "content", None) for p in getattr(result, "paragraphs", [])],
        "tables": [getattr(t, "row_count", None) for t in getattr(result, "tables", [])],
        "styles": len(getattr(result, "styles", []) or []),
    })


def normalize_table_result(result: Any) -> NormalizedDocumentResult:
    tables = []
    for table in getattr(result, "tables", []) or []:
        cells = []
        for cell in getattr(table, "cells", []) or []:
            cells.append({
                "row_index": getattr(cell, "row_index", None),
                "column_index": getattr(cell, "column_index", None),
                "content": getattr(cell, "content", None),
                "row_span": getattr(cell, "row_span", None),
                "column_span": getattr(cell, "column_span", None),
            })
        tables.append({"row_count": getattr(table, "row_count", None), "column_count": getattr(table, "column_count", None), "cells": cells})
    return NormalizedDocumentResult(raw=result, data={"tables": tables})


def normalize_key_values_result(result: Any) -> NormalizedDocumentResult:
    pairs = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        pairs.append({
            "key": getattr(getattr(kv, "key", None), "content", None),
            "value": getattr(getattr(kv, "value", None), "content", None),
        })
    return NormalizedDocumentResult(raw=result, data={"key_value_pairs": pairs})
