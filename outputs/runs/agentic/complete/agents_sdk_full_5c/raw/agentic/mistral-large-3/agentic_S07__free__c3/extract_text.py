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
    request_payload = {
        "requests": [
            {
                "image": {"content": content},
                "features": [{"type": "TEXT_DETECTION"}],
                "imageContext": {"languageHints": ["en"]}
            }
        ]
    }
    
    response = requests.post(
        f"https://vision.googleapis.com/v1/images:annotate?key={os.getenv('GOOGLE_CLOUD_VISION_API_KEY')}",
        json=request_payload
    )
    response.raise_for_status()
    
    result = response.json()
    full_text = result["responses"][0].get("fullTextAnnotation", {}).get("text", "")
    
    return TextExtractionResponse(
        text=full_text,
        provider="google_cloud_vision",
        raw_response=result
    )