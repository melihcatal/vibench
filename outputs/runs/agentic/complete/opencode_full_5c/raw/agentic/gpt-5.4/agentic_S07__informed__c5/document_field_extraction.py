from __future__ import annotations

from document_client import DEFAULT_INVOICE_MODEL, create_document_client, read_bytes


def extract_document_fields(file_path: str) -> dict:
    client = create_document_client()
    poller = client.begin_analyze_document(
        DEFAULT_INVOICE_MODEL, body=read_bytes(file_path)
    )
    result = poller.result()
    documents = []
    for document in getattr(result, "documents", []) or []:
        fields = {}
        for name, field in (getattr(document, "fields", None) or {}).items():
            fields[name] = {
                "value": getattr(field, "value", None),
                "content": getattr(field, "content", None),
                "confidence": getattr(field, "confidence", None),
                "value_type": str(getattr(field, "value_type", "unknown")),
            }
        documents.append(
            {
                "doc_type": getattr(document, "doc_type", None),
                "confidence": getattr(document, "confidence", None),
                "fields": fields,
            }
        )
    return {
        "provider": "azure-document-intelligence",
        "model_id": DEFAULT_INVOICE_MODEL,
        "documents": documents,
    }
