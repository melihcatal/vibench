from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, get_invoice_model_id
from document_models import as_dict


def extract_document_fields(file_bytes: bytes) -> dict:
    client = get_document_intelligence_client()
    model_id = get_invoice_model_id()
    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=file_bytes),
    )
    result = poller.result()
    documents = []
    for document in result.documents or []:
        fields = {}
        for name, field in (document.fields or {}).items():
            fields[name] = {
                "content": getattr(field, "content", None),
                "value": getattr(field, "value_string", None)
                or getattr(field, "value_date", None)
                or getattr(field, "value_time", None)
                or getattr(field, "value_currency", None)
                or getattr(field, "value_number", None)
                or getattr(field, "value_integer", None),
                "confidence": getattr(field, "confidence", None),
                "type": getattr(field, "type", None),
            }
        documents.append(
            {
                "doc_type": document.doc_type,
                "fields": fields,
                "confidence": document.confidence,
            }
        )
    return {
        "provider": "azure-ai-documentintelligence",
        "model_id": model_id,
        "documents": documents,
        "raw": as_dict(result),
    }
