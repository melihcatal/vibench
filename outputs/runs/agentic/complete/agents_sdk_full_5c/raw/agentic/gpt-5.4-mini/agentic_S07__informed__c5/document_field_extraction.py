from __future__ import annotations

from typing import Dict

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import begin_analyze_document


def extract_structured_fields(document) -> Dict[str, str]:
    poller = begin_analyze_document("prebuilt-invoice", document, content_type="application/octet-stream")
    result = poller.result()
    fields: Dict[str, str] = {}
    doc = (getattr(result, "documents", []) or [{}])[0]
    if hasattr(doc, "fields"):
        for name, field in doc.fields.items():
            value = getattr(field, "content", None) or getattr(field, "value", None)
            if value is not None:
                fields[name] = str(value)
    return fields
