import os
from typing import Dict, Any, List
import requests
from document_models import SafetyCheckResponse


def check_text_safety(text: str) -> SafetyCheckResponse:
    """
    Check extracted document text for unsafe content using Google Cloud Natural Language API.
    """
    api_key = os.getenv("GOOGLE_CLOUD_NATURAL_LANGUAGE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_NATURAL_LANGUAGE_API_KEY environment variable not set")
    
    # Google Cloud Natural Language API-specific request for content safety
    request_payload = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": text
        },
        "encodingType": "UTF8"
    }
    
    response = requests.post(
        f"https://language.googleapis.com/v1/documents:moderateText?key={api_key}",
        json=request_payload
    )
    response.raise_for_status()
    
    result = response.json()
    moderation_categories = result.get("moderationCategories", [])
    unsafe_categories = [
        category["name"] for category in moderation_categories if category.get("confidence", 0) > 0.5
    ]
    
    return SafetyCheckResponse(
        is_safe=len(unsafe_categories) == 0,
        unsafe_categories=unsafe_categories,
        provider="google_cloud_natural_language",
        raw_response=result
    )