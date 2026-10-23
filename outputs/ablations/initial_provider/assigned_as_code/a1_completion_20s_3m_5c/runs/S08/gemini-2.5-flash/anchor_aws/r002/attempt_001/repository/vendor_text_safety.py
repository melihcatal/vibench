import os
from google.cloud import language_v1
from typing import Dict, Any
from document_models import NormalizedExpense

def moderate_vendor_text_safety(text_content: str, expense: NormalizedExpense, config=None) -> Dict[str, Any]:
    config = config or {}
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classifying content to get safety attributes
    # Note: Content Classification is not the same as the specialized 'Cloud Content Safety' API.
    # For this exercise, we will use general content classification as a proxy for safety analysis.
    # In a real-world scenario, the dedicated Content Safety API would be preferred.
    response = client.classify_text(request = {'document': document})
    
    safety_scores = {"categories": []}
    for category in response.categories:
        safety_scores["categories"].append({"name": category.name, "confidence": category.confidence})
    
    # Placeholder for more specific safety checks if a dedicated API were used.
    # For instance, checking for specific types of harmful content.

    expense.safety_scores = safety_scores
    return safety_scores
