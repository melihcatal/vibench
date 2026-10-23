import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import KeyValueExtractionResponse, KeyValuePair


def extract_key_values(image_path: str) -> KeyValueExtractionResponse:
    """
    Extract key-value pairs from a form-like document using Google Document AI.
    """
    client = get_document_client("document_ai")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Google Document AI-specific request
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION")
    
    response = client.post(
        f"https://{location}-documentai.googleapis.com/v1/projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/{location}/processors/{processor_id}:process",
        json={
            "rawDocument": {
                "content": content,
                "mimeType": "application/pdf"
            }
        }
    )
    
    response.raise_for_status()
    result = response.json()
    
    # Normalize response to local model
    key_values = []
    for entity in result.get("document", {}).get("entities", []):
        if entity.get("type") == "form_field":
            key = entity.get("properties", [{}])[0].get("textAnchor", {}).get("content", "")
            value = entity.get("textAnchor", {}).get("content", "")
            key_values.append(KeyValuePair(key=key, value=value))
    
    return KeyValueExtractionResponse(key_values=key_values, provider="google_document_ai")