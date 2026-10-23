from __future__ import annotations

from document_client import get_document_intelligence_client
from document_models import (
    DocumentSource,
    StructuredFieldExtractionResult,
    load_binary,
    normalize_text,
)


def extract_document_fields(source: DocumentSource) -> StructuredFieldExtractionResult:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=load_binary(source),
    )
    result = poller.result()
    fields = {}
    for document in result.documents or []:
        for name, field in (document.fields or {}).items():
            value = getattr(field, "value", None)
            if value is None:
                value = getattr(field, "content", None)
            fields[name] = normalize_text(str(value)) if value is not None else ""
    return StructuredFieldExtractionResult(
        provider="azure-ai-documentintelligence", fields=fields, raw=result
    )
