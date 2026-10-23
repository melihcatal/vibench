from typing import Any, Dict

from google.cloud import documentai_v1 as documentai


def extract_document_fields(document_text: str, *, project_id: str, location: str, processor_id: str) -> Dict[str, Any]:
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    doc = documentai.RawDocument(content=document_text.encode("utf-8"), mime_type="text/plain")
    response = client.process_document(name=name, raw_document=doc)
    document = response.document
    fields = {}
    for entity in document.entities:
        fields.setdefault(entity.type_, []).append(entity.mention_text)
    return {"provider": "google-document-ai", "fields": fields, "raw": response}
