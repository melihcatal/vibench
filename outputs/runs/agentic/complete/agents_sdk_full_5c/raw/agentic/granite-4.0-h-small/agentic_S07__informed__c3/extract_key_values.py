# [SAME-SCENARIO] extract_key_values.py

import os
from document_client import DocumentOcrClient

def extract_key_values_from_image(image_path: str) -> dict:
    """Extract key-value pairs from a form-like document image.

    Uses Azure AI Document Intelligence (prebuilt form recognizer) to detect field names and values.
    Environment variables:
        - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
        - AZURE_DOCUMENT_INTELLIGENCE_KEY
    Returns a dict mapping each recognized field name to its extracted value.
    """
    client = DocumentOcrClient(service=\"azure_document_intelligence\")
    response = client.analyze_form(image_path, model_id=\"prebuilt-form\")
    kv_pairs = {}
    for result in response.get(\"analyzeResult\", {}).get(\"documentResults\", []):
        for field in result.get(\"fields\", []):
            name = field.get(\"name\")
            value = field.get(\"valueString\")
            kv_pairs[name] = value
    return kv_pairs
