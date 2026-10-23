from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_INVOICE_MODEL, get_document_client


def extract_document_fields(document_path: str) -> Dict[str, Any]:
    client = get_document_client()
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=DEFAULT_INVOICE_MODEL,
            body=AnalyzeDocumentRequest(bytes_source=f.read()),
        )
    result = poller.result()

    documents: List[Dict[str, Any]] = []
    for doc in result.documents or []:
        fields: Dict[str, Any] = {}
        for name, field in (doc.fields or {}).items():
            fields[name] = {
                "value": getattr(field, "value", None),
                "content": getattr(field, "content", None),
                "confidence": getattr(field, "confidence", None),
                "type": str(getattr(field, "type", "")),
            }
        documents.append({
            "doc_type": doc.doc_type,
            "confidence": doc.confidence,
            "fields": fields,
        })

    return {
        "provider": "azure-document-intelligence",
        "model_id": DEFAULT_INVOICE_MODEL,
        "documents": documents,
    }
