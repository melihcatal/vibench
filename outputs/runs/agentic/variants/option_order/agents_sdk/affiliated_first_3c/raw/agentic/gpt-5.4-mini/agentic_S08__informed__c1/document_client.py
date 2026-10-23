from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from document_models import DocumentExtractionResult, DocumentField, LineItem

AZURE_ENDPOINT_ENV = "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
AZURE_KEY_ENV = "AZURE_DOCUMENT_INTELLIGENCE_KEY"


@dataclass
class DocumentClientConfig:
    endpoint: str
    key: str
    model_id: str = "prebuilt-invoice"


def load_config() -> DocumentClientConfig:
    endpoint = os.getenv(AZURE_ENDPOINT_ENV, "")
    key = os.getenv(AZURE_KEY_ENV, "")
    return DocumentClientConfig(endpoint=endpoint, key=key)


def build_azure_invoice_client() -> Any:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    cfg = load_config()
    return DocumentIntelligenceClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def parse_invoice_result(result: Any) -> DocumentExtractionResult:
    fields: Dict[str, DocumentField] = {}
    line_items = []
    raw = getattr(result, "as_dict", lambda: {})()

    doc = None
    documents = getattr(result, "documents", None) or []
    if documents:
        doc = documents[0]

    if doc and getattr(doc, "fields", None):
        for name, field in doc.fields.items():
            fields[name] = DocumentField(name=name, value=getattr(field, "value", None), confidence=float(getattr(field, "confidence", 0.0) or 0.0))

    for item in getattr(result, "documents", [])[:1]:
        for li in getattr(item, "fields", {}).get("Items", []) if getattr(item, "fields", None) else []:
            line_items.append(
                LineItem(
                    description=normalize_line_description(li),
                    quantity=None,
                    unit_price=None,
                    amount=None,
                    confidence=float(getattr(li, "confidence", 0.0) or 0.0),
                )
            )

    return DocumentExtractionResult(provider="azure-document-intelligence-prebuilt-invoice", fields=fields, line_items=line_items, raw=raw)


def normalize_line_description(item: Any) -> str:
    if isinstance(item, dict):
        for key in ("description", "Description", "Name", "value"):
            if key in item and item[key]:
                return str(item[key])
    return str(getattr(item, "content", "")).strip()


def extract_document_fields(file_bytes: bytes, model_id: Optional[str] = None) -> DocumentExtractionResult:
    client = build_azure_invoice_client()
    cfg = load_config()
    model = model_id or cfg.model_id
    poller = client.begin_analyze_document(model, body=file_bytes)
    result = poller.result()
    return parse_invoice_result(result)
