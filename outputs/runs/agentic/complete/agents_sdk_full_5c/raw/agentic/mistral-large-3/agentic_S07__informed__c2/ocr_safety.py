from typing import List, Optional
import os
import requests
from document_models import SafetyCheckResponse


def check_text_safety(text: str) -> SafetyCheckResponse:
    """Check extracted document text for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "must be set in environment variables."
        )
    
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "breakByBlock": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    violations = []
    
    for category in result.get("categoriesAnalysis", []):
        if category.get("severity", 0) > 2:
            violations.append(category["category"])
    
    return SafetyCheckResponse(
        is_safe=len(violations) == 0,
        violations=violations,
        confidence=1.0 - (len(violations) / len(result.get("categoriesAnalysis", [])))
    )