import os
from google.cloud import documentai_v1 as documentai

# Helper client utilities loaded from document_client.py
from document_client import DocumentClient


def extract_layout(file_path: str):
    """Extract layout elements (blocks, lines, tables) from a document image using Google Document AI.

    Returns:
        A dict containing layout elements and their positions.
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
    # Convert to normalized layout model defined in document_models.py
    from document_models import layout_from_response

    return layout_from_response(response.document)
