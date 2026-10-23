"""
Moderate a batch of user messages using Azure AI Content Safety.
"""
from typing import List, Dict

from safety_client import AzureContentSafetyClient
from safety_models import SafetyRequest, SafetyResponse


client = AzureContentSafetyClient()


def moderate_batch(texts: List[str], categories: Optional[List[str]] = None) -> List[Dict]:
    """Moderate a batch of user messages."""
    results = []
    for text in texts:
        request: SafetyRequest = {
            "text": text,
            "categories": categories,
            "threshold": None
        }
        response: SafetyResponse = client.moderate(request)
        results.append({
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
        })
    return results