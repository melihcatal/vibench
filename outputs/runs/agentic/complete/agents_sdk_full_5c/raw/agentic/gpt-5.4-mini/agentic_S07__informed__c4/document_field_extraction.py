from __future__ import annotations

from typing import Dict

from google.cloud import documentai

from document_models import FieldExtractionResult, normalize_text


def extract_document_fields(file_path: str, processor_name: str, mime_type: str = "image/png") -> FieldExtractionResult:
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as handle:
        raw_document = documentai.RawDocument(content=handle.read(), mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)
    fields: Dict[str, str] = {}
    document = response.document
    for page in getattr(document, "pages", []):
        for kv in getattr(page, "form_fields", []):
            key = normalize_text(getattr(getattr(kv, "field_name", None), "text_anchor", {}))
            value = normalize_text(getattr(getattr(kv, "field_value", None), "text_anchor", {}))
            if key:
                fields[key] = value
    return FieldExtractionResult(fields=fields, raw=response)
