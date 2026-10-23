from document_client import get_document_intelligence_client
from document_models import ExtractedTableResult, DocumentProcessingRequest
import io

def extract_tables(request: DocumentProcessingRequest) -> ExtractedTableResult:
    """
    Extracts table cells and row structure from a document using Azure Document Intelligence.
    Uses the prebuilt-layout model which includes table extraction.
    """
    client = get_document_intelligence_client()

    if request.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-layout", document_url=request.document_url
        )
    elif request.document_content and request.content_type:
        document_stream = io.BytesIO(request.document_content)
        poller = client.begin_analyze_document(
            "prebuilt-layout", document_stream, content_type=request.content_type
        )
    else:
        raise ValueError("Either document_url or document_content and content_type must be provided.")

    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table in result.tables:
            cells_data = []
            for cell in table.cells:
                cells_data.append({
                    "content": cell.content,
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "row_span": cell.row_span,
                    "column_span": cell.column_span,
                    "kind": str(cell.kind.value) if cell.kind else None
                })
            extracted_tables.append({
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": cells_data
            })

    return ExtractedTableResult(tables=extracted_tables)
