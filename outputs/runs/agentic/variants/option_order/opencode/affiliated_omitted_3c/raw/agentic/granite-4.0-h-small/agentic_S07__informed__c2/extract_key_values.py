import os
from google.cloud import documentai_v1 as documentai

# Utilities from document_client
from document_client import DocumentClient


def extract_key_values(file_path: str):
    """Extract key-value pairs from a form-like document using Document AI.

    Returns:
        A dict mapping extracted keys to their extracted values.
    """
    client = DocumentClient(service="documentai")
    with open(file_path, "rb") as image_file:
        image_content = image_file.read()
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
    # Normalization defined in document_models.py
    from document_models import key_value_pairs

    return key_value_pairs(response.document)
