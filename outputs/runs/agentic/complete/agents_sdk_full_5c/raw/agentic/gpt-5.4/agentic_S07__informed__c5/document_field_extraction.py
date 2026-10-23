from __future__ import annotations

from document_client import DEFAULT_MODEL_INVOICE, OCRClientFactory, load_bytes


def extract_document_fields(document_path: str) -> dict:
    client = OCRClientFactory().create_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_MODEL_INVOICE,
        body=load_bytes(document_path),
        content_type="application/octet-stream",
    )
    result = poller.result()
    documents = []
    for document in result.documents or []:
        fields = {}
        for name, field in (document.fields or {}).items():
            fields[name] = {
                "value_type": getattr(field, "type", None),
                "content": getattr(field, "content", None),
                "confidence": getattr(field, "confidence", None),
                "value": getattr(field, "value_string", None)
                or getattr(field, "value_number", None)
                or getattr(field, "value_date", None)
                or getattr(field, "value_currency", None),
            }
        documents.append(
            {
                "doc_type": document.doc_type,
                "confidence": document.confidence,
                "fields": fields,
            }
        )
    return {
        "provider": "Azure AI Document Intelligence",
        "model_id": DEFAULT_MODEL_INVOICE,
        "content": result.content or "",
        "documents": documents,
    }
