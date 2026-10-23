from typing import Dict, List, Optional

from document_client import AzureDocumentIntelligenceClient, get_default_client
from document_models import TableRequest, TableResponse, normalize_document_result

AZURE_DOC_INTELLIGENCE_MODEL_ID = "prebuilt-layout"


def _build_payload(request: TableRequest) -> Dict[str, object]:
    if request.image_url:
        return {"urlSource": request.image_url}
    if request.image_bytes_b64:
        return {"base64Source": request.image_bytes_b64}
    return {}


def extract_tables(request: TableRequest, client: Optional[AzureDocumentIntelligenceClient] = None) -> TableResponse:
    client = client or get_default_client()
    response = client.post_analyze(AZURE_DOC_INTELLIGENCE_MODEL_ID, _build_payload(request))
    response.raise_for_status()
    operation_url = response.headers.get("operation-location")
    result = client.get_operation(operation_url)
    result.raise_for_status()
    raw = result.json()
    normalized = normalize_document_result(raw)
    tables: List[Dict[str, object]] = []
    for table in normalized["tables"]:
        cells = table.get("cells", [])
        row_count = max((cell.get("rowIndex", 0) for cell in cells), default=0) + 1 if cells else 0
        tables.append({"row_count": row_count, "cells": cells, **table})
    return TableResponse(tables=tables, raw=raw)
