from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_INVOICE_MODEL, get_document_intelligence_client, load_document_bytes


def extract_document_fields(document_path: str) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_INVOICE_MODEL,
        body=load_document_bytes(document_path),
    )
    result = poller.result()

    documents: List[Dict[str, Any]] = []
    for analyzed_document in result.documents or []:
        fields: Dict[str, Any] = {}
        for name, field in (analyzed_document.fields or {}).items():
            fields[name] = {
                "value_type": getattr(field, "value_type", None),
                "content": getattr(field, "content", None),
                "confidence": getattr(field, "confidence", None),
                "value": getattr(field, "value_string", None)
                or getattr(field, "value_currency", None)
                or getattr(field, "value_date", None)
                or getattr(field, "value_number", None)
                or getattr(field, "value_integer", None)
                or getattr(field, "value_phone_number", None),
            }
        documents.append({
            "doc_type": analyzed_document.doc_type,
            "confidence": analyzed_document.confidence,
            "fields": fields,
        })

    return {
        "provider": "azure-ai-documentintelligence",
        "model_id": DEFAULT_INVOICE_MODEL,
        "documents": documents,
    }
