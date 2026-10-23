"""
Moderate user text for unsafe or policy-violating content using Azure AI Content Safety.
"""
from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest


def moderate_text(text: str) -> dict:
    """Score user text for unsafe content."""
    client = AzureContentSafetyClient()
    request = TextModerationRequest(text=text)
    response = client.moderate_text(request)
    return {
        "flagged": response.is_flagged(),
        "decisions": [
            {
                "category": decision["category"].value,
                "score": decision["score"],
                "flagged": decision["flagged"],
            }
            for decision in response.decisions
        ],
        "raw_response": response.raw_response,
    }