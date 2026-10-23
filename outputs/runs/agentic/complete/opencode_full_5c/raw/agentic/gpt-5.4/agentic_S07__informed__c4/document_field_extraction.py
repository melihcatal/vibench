from __future__ import annotations

from io import BytesIO

from document_client import DEFAULT_INVOICE_MODEL, get_document_intelligence_client
from document_models import FieldExtractionResult, StructuredField, normalize_text


def extract_document_fields(
    document_bytes: bytes, mime_type: str
) -> FieldExtractionResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id=DEFAULT_INVOICE_MODEL,
        body=BytesIO(document_bytes),
        content_type=mime_type,
    )
    result = poller.result()
    fields = []
    for document in result.documents or []:
        for name, field in (document.fields or {}).items():
            fields.append(
                StructuredField(
                    name=name,
                    value=normalize_text(
                        getattr(field, "content", None)
                        or getattr(field, "value_string", None)
                        or str(getattr(field, "value", ""))
                    ),
                    confidence=getattr(field, "confidence", None),
                )
            )
    return FieldExtractionResult(
        provider="azure-document-intelligence",
        fields=fields,
        raw=result,
    )
