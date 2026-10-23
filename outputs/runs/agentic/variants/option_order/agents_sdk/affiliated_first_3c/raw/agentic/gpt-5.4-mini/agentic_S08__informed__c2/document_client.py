from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import ExtractionRequest, ExtractionResponse, LineItem

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


def build_client() -> DocumentIntelligenceClient:
    if not AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or not AZURE_DOCUMENT_INTELLIGENCE_KEY:
        raise ValueError("Azure Document Intelligence credentials are required")
    return DocumentIntelligenceClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY),
    )


def request_payload(req: ExtractionRequest) -> Dict[str, Any]:
    payload = {"source_uri": req.source_uri, "filename": req.filename, "metadata": req.metadata}
    if req.content is not None:
        payload["content_length"] = len(req.content)
    return payload


def response_from_result(result: Any, provider: str) -> ExtractionResponse:
    fields: Dict[str, Any] = {}
    line_items = []
    raw = {}
    if hasattr(result, "as_dict"):
        raw = result.as_dict()
    elif isinstance(result, dict):
        raw = result
    if raw:
        fields = raw.get("fields", raw.get("documents", {})) if isinstance(raw, dict) else {}
        for item in raw.get("line_items", []):
            line_items.append(LineItem(**item))
    return ExtractionResponse(fields=fields, line_items=line_items, raw=raw, provider=provider)


def as_record(response: ExtractionResponse) -> Dict[str, Any]:
    return {"provider": response.provider, "fields": response.fields, "line_items": [asdict(item) for item in response.line_items], "raw": response.raw}
