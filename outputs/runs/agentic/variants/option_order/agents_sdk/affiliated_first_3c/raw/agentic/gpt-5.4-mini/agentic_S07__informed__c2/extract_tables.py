from __future__ import annotations

from typing import List, Union

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_client
from document_models import DocumentInput, TableCell, TableExtractionResult

PROVIDER = "azure-document-intelligence"
MODEL_ID = "prebuilt-layout"


def extract_tables(document: Union[DocumentInput, str]) -> TableExtractionResult:
    client = get_client()
    source_url = document.source_url if isinstance(document, DocumentInput) else str(document)
    poller = client.begin_analyze_document(model_id=MODEL_ID, analyze_request=AnalyzeDocumentRequest(url_source=source_url))
    result = poller.result()
    tables: List[List[TableCell]] = []
    for table in getattr(result, "tables", []) or []:
        cells: List[TableCell] = []
        for cell in getattr(table, "cells", []) or []:
            cells.append(
                TableCell(
                    row_index=getattr(cell, "row_index", 0),
                    column_index=getattr(cell, "column_index", 0),
                    content=getattr(cell, "content", "") or "",
                    row_span=getattr(cell, "row_span", 1),
                    column_span=getattr(cell, "column_span", 1),
                )
            )
        tables.append(cells)
    return TableExtractionResult(tables=tables, provider=PROVIDER, model_id=MODEL_ID)
