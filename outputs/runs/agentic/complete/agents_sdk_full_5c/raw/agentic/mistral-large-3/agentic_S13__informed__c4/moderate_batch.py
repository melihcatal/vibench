"""
Moderate a batch of user messages using Azure AI Content Safety.
"""
from typing import List
from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest


def moderate_batch(texts: List[str]) -> List[dict]:
    """Moderate a batch of user messages."""
    client = AzureContentSafetyClient()
    results = []
    for text in texts:
        request = TextModerationRequest(text=text)
        response = client.moderate_text(request)
        results.append({
            "text": text,
            "flagged": response.is_flagged(),
            "decisions": [
                {
                    "category": decision["category"].value,
                    "score": decision["score"],
                    "flagged": decision["flagged"],
                }
                for decision in response.decisions
            ],
        })
    return results