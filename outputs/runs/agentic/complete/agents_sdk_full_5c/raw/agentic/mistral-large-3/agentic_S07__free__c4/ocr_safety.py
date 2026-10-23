import os
from typing import Dict, Any
import requests
from document_models import SafetyCheckResponse


def check_text_safety(text: str) -> SafetyCheckResponse:
    """
    Check extracted document text for unsafe content using Google Cloud Natural Language API.
    """
    response = requests.post(
        f"https://language.googleapis.com/v1/documents:analyzeText?key={os.getenv('GOOGLE_CLOUD_API_KEY')}",
        json={
            "document": {
                "type": "PLAIN_TEXT",
                "content": text
            },
            "encodingType": "UTF8",
            "features": {
                "extractDocumentSentiment": False,
                "classifyText": True
            }
        }
    )
    
    response.raise_for_status()
    result = response.json()
    
    unsafe_categories = []
    for category in result.get("categories", []):
        if category["confidence"] > 0.7 and category["name"] in [
            "/Adult", 
            "/Violence", 
            "/Religion & Beliefs",
            "/Illegal Drugs"
        ]:
            unsafe_categories.append(category["name"])
    
    return SafetyCheckResponse(
        is_safe=len(unsafe_categories) == 0,
        unsafe_categories=unsafe_categories,
        provider="google_cloud_natural_language"
    )