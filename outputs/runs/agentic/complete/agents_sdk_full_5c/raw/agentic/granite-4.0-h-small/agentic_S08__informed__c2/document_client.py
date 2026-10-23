import os
from typing import Any

# Example helper using Google Cloud Document AI (similar patterns for other providers)

def get_document_client() -> Any:
    # Load credentials from environment (GOOGLE_APPLICATION_CREDENTIALS expected)
    from google.cloud import documentai_v1 as documentai
    return documentai.DocumentProcessorServiceClient()


def process_document_with_client(client, processor_id: str, file_bytes: bytes, mime_type: str = "application/pdf") -> Any:
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/{processor_id}"
    raw_doc = documentai.RawDocument(content=file_bytes, mime_type=mime_type)
    response = client.process_document(name=processor_name, raw_document=raw_doc)
    return response.document
