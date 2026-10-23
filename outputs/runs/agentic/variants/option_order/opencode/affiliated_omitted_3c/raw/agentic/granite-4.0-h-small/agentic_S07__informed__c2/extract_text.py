import os
from google.cloud import documentai_v1 as documentai

# Helper client utilities loaded from document_client.py
from document_client import DocumentClient


def extract_text(file_path: str) -> str:
    """Extract plain text from a scanned document image using Google Document AI.

    Returns:
        The extracted plain text.
    """
    client = DocumentClient(service="documentai")
    # Load image bytes
    with open(file_path, "rb") as image_file:
        image_content = image_file.read()
    # Call provider SDK
    response = client.client.documents.process_document(
        request={
            "name": client.processor,
            "input_config": {
                "mimeType": "image/jpeg",
                "document": {
                    "content": image_content,
                },
            },
        }
    )
    # Normalization utility from document_models.py
    from document_models import normalize_processed_document

    return normalize_processed_document(response.document)
