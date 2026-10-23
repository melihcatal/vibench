from __future__ import annotations

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, guess_content_type, read_bytes
from document_models import normalize_text


def extract_invoice_fields(document_path: str) -> dict:
    client = get_document_intelligence_client()
    payload = read_bytes(document_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=AnalyzeDocumentRequest(bytes_source=payload),
        content_type=guess_content_type(document_path),
    )
    result = poller.result()

    documents = []
    for document in result.documents or []:
        fields = {}
        for name, field in (document.fields or {}).items():
            fields[name] = {
                "content": normalize_text(getattr(field, "content", None)),
                "value_type": getattr(field, "type", None),
                "confidence": getattr(field, "confidence", None),
                "value": getattr(field, "value_string", None)
                or getattr(field, "value_currency", None)
                or getattr(field, "value_date", None)
                or getattr(field, "value_number", None),
            }
        documents.append(
            {
                "doc_type": document.doc_type,
                "confidence": document.confidence,
                "fields": fields,
            }
        )

    return {
        "provider": "azure-ai-documentintelligence:prebuilt-invoice",
        "documents": documents,
        "raw": result,
    }
