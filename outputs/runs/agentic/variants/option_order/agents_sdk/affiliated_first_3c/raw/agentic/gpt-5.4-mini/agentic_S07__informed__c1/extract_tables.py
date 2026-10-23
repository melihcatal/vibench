from __future__ import annotations

from typing import Optional

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, load_config
from document_models import DocumentInput, TableResult


def extract_tables(document: DocumentInput, model_id: Optional[str] = None) -> TableResult:
    cfg = load_config(model_id=model_id or document.model or "prebuilt-layout", locale=document.locale)
    client = build_client(cfg)
    poller = client.begin_analyze_document(
        model_id=cfg.model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document.content),
        content_type=document.content_type,
        locale=cfg.locale,
    )
    result = poller.result()
    tables = []
    for table in getattr(result, "tables", []) or []:
        cells = []
        for cell in getattr(table, "cells", []) or []:
            cells.append({
                "row_index": getattr(cell, "row_index", None),
                "column_index": getattr(cell, "column_index", None),
                "content": getattr(cell, "content", None),
                "kind": getattr(cell, "kind", None),
            })
        tables.append({"row_count": getattr(table, "row_count", None), "column_count": getattr(table, "column_count", None), "cells": cells})
    return TableResult(tables=tables, raw=result)
