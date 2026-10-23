import os
from typing import Dict, Any
import requests
from document_models import SafetyCheckResponse


def check_text_safety(text: str) -> SafetyCheckResponse:
    """
    Check extracted document text for unsafe content using Google Cloud Natural Language API.
    """
    api_key = os.getenv("GOOGLE_CLOUD_NATURAL_LANGUAGE_API_KEY")
    
    # Google Cloud Natural Language API-specific request for content safety
    request_payload = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": text
        },
        "encodingType": "UTF8"
    }
    
    response = requests.post(
        f"https://language.googleapis.com/v1/documents:analyzeSentiment?key={api_key}",
        json=request_payload
    )
    response.raise_for_status()
    sentiment_result = response.json()

    # Google Cloud Natural Language API for content moderation
    response = requests.post(
        f"https://language.googleapis.com/v1/documents:moderateText?key={api_key}",
        json=request_payload
    )
    response.raise_for_status()
    moderation_result = response.json()
    
    unsafe_categories = []
    for category in moderation_result.get("moderationCategories", []):
        if category.get("confidence", 0.0) > 0.7:
            unsafe_categories.append(category.get("name", ""))
    
    is_safe = len(unsafe_categories) == 0
    
    return SafetyCheckResponse(
        is_safe=is_safe,
        unsafe_categories=unsafe_categories,
        provider="google_cloud_natural_language",
        raw_response={
            "sentiment": sentiment_result,
            "moderation": moderation_result
        }
    )