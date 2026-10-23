from __future__ import annotations

from typing import Optional

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client, load_config
from document_models import DocumentInput, LayoutResult


def extract_layout(document: DocumentInput, model_id: Optional[str] = None) -> LayoutResult:
    cfg = load_config(model_id=model_id or document.model or "prebuilt-layout", locale=document.locale)
    client = build_client(cfg)
    poller = client.begin_analyze_document(
        model_id=cfg.model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document.content),
        content_type=document.content_type,
        locale=cfg.locale,
    )
    result = poller.result()
    blocks = []
    lines = []
    tables = []
    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            lines.append({"content": getattr(line, "content", None), "polygon": getattr(line, "polygon", None)})
    for paragraph in getattr(result, "paragraphs", []) or []:
        blocks.append({"content": getattr(paragraph, "content", None), "role": getattr(paragraph, "role", None)})
    for table in getattr(result, "tables", []) or []:
        tables.append({"row_count": getattr(table, "row_count", None), "column_count": getattr(table, "column_count", None), "cells": getattr(table, "cells", None)})
    return LayoutResult(blocks=blocks, lines=lines, tables=tables, raw=result)
