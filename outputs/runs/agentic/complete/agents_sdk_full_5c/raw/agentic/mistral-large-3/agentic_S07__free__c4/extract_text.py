import os
from typing import Dict, Any
import requests
from document_client import get_document_client
from document_models import TextExtractionResponse


def extract_text(image_path: str) -> TextExtractionResponse:
    """
    Extract plain text from a scanned document image using Google Cloud Vision API.
    """
    client = get_document_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Google Cloud Vision API-specific request
    response = client.post(
        f"https://vision.googleapis.com/v1/projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/{os.getenv('GOOGLE_CLOUD_LOCATION')}/files:annotate",
        json={
            "requests": [
                {
                    "image": {"content": content},
                    "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                }
            ]
        },
        headers={"x-goog-user-project": os.getenv("GOOGLE_CLOUD_PROJECT_ID")},
    )
    
    response.raise_for_status()
    result = response.json()
    
    # Normalize response to local model
    full_text = result["responses"][0].get("fullTextAnnotation", {}).get("text", "")
    return TextExtractionResponse(text=full_text, provider="google_cloud_vision")