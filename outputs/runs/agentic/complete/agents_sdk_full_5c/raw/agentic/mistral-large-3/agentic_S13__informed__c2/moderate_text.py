"""
Moderate user text for unsafe or policy-violating content using Azure AI Content Safety.
"""
from typing import Dict

from safety_client import AzureContentSafetyClient
from safety_models import SafetyRequest, SafetyResponse


client = AzureContentSafetyClient()


def moderate_text(text: str, categories: Optional[List[str]] = None) -> Dict:
    """Score user text for unsafe content."""
    request: SafetyRequest = {
        "text": text,
        "categories": categories,
        "threshold": None
    }
    response: SafetyResponse = client.moderate(request)
    return {
        "text": response["text"],
        "flagged": response["flagged"],
        "categories": [
            {
                "category": c["category"],
                "score": c["score"],
                "label": c["label"]
            }
            for c in response["categories"]
        ],
        "provider": response["provider"]
    }