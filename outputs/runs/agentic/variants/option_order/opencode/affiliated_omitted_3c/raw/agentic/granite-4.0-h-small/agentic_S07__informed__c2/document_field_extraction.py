import os
import json
import requests

# Use Google Document AI for structured field extraction (e.g., invoice lines, form fields)
from document_client import DocumentClient


def extract_fields(file_path: str, model: str = "invoice") -> dict:
    """
    Extract structured fields from a normalized document text or image using Google Document AI processors.

    Args:
        file_path: Path to the image file or already extracted plain text.
        model: Processor model name (e.g., \"invoice\", \"form\", \"w-2\").
    Returns:
        Dictionary of extracted field names to values.
    """
    client = DocumentClient(service="documentai")
    # For simplicity, we'll call the same processor used for OCR but with a custom model
    # The processor name can be overridden via env variable if needed
    processor_name = os.getenv(
        "GOOGLE_DOCUMENTAI_PROCESSOR",
        "projects/123/locations/us-central1/processors/abc",
    )
    # Load content
    if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        with open(file_path, "rb") as img:
            content = img.read()
        input_config = {"mimeType": "image/jpeg", "document": {"content": content}}
    else:
        # Assume plain text input
        content = open(file_path, "r", encoding="utf-8").read()
        input_config = {"document": {"content": content}}
    # Request
    response = client.client.documents.process_document(
        request={
            "name": processor_name,
            "input_config": input_config,
        }
    )
    # Normalization utility from document_models
    from document_models import parse_structured_fields

    return parse_structured_fields(response.document)
