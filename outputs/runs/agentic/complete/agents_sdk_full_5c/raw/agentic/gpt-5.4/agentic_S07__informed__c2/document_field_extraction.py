from __future__ import annotations

from typing import Dict, List

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_INVOICE_MODEL, get_document_client, load_document_bytes


def extract_document_fields(document_path: str, model_id: str = DEFAULT_INVOICE_MODEL) -> Dict[str, object]:
    client = get_document_client()
    body = AnalyzeDocumentRequest(bytes_source=load_document_bytes(document_path))
    poller = client.begin_analyze_document(model_id=model_id, body=body)
    result = poller.result()

    documents_out: List[Dict[str, object]] = []
    for document in result.documents or []:
        fields = {}
        for name, field in (getattr(document, "fields", None) or {}).items():
            fields[name] = {
                "content": getattr(field, "content", None),
                "value_type": getattr(field, "type", None),
                "confidence": getattr(field, "confidence", None),
                "value": getattr(field, "value_string", None)
                or getattr(field, "value_number", None)
                or getattr(field, "value_date", None)
                or getattr(field, "value_currency", None),
            }
        documents_out.append(
            {
                "doc_type": getattr(document, "doc_type", None),
                "confidence": getattr(document, "confidence", None),
                "fields": fields,
            }
        )

    return {
        "provider": "azure-document-intelligence",
        "model_id": model_id,
        "documents": documents_out,
    }
