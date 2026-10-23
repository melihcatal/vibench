import os
import json
from document_client import OcrClient


def extract_key_values(image_path: str) -> dict:
    """Extract key-value pairs from a form-like document.

    Uses Google Document AI processors for forms. Set GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    client = OcrClient()  # Google Document AI client
    response = client.process_document(
        document_data={"content": open(image_path, "rb").read()}
    )
    # Normalize form fields
    kv_pairs = {}
    for field in response.document.pages[0].content[0].paragraphs[0].tokens:
        # Simplistic parsing: assume field name followed by value
        kv_pairs[field.text] = (
            field.text
        )  # placeholder - real parsing depends on provider schema
    return kv_pairs
