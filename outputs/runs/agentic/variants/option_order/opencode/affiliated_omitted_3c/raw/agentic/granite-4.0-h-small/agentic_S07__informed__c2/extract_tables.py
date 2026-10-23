import os
from google.cloud import documentai_v1 as documentai

# Helper utilities from document_client
from document_client import DocumentClient


def extract_tables(file_path: str):
    """Extract tables (cells and row structure) from a document image using Document AI.

    Returns:
        List of tables where each table is represented as a list of rows,
        and each row is a list of cell values.
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
    # Normalization function from document_models.py
    from document_models import tables_from_document

    return tables_from_document(response.document)
