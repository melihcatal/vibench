from typing import Dict, List

from google.cloud import documentai


def extract_document_fields(text: str, processor_name: str) -> Dict[str, object]:
    client = documentai.DocumentProcessorServiceClient()
    document = documentai.Document.from_json({"text": text})
    return {"processor_name": processor_name, "text": document.text, "fields": []}
