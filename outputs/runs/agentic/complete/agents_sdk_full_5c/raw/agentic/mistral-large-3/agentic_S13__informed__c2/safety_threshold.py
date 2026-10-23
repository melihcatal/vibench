"""
Apply category thresholds to decide whether to allow text using Azure AI Content Safety.
"""
from typing import Dict, List, Optional

from safety_client import AzureContentSafetyClient
from safety_models import SafetyRequest, SafetyResponse


client = AzureContentSafetyClient()


def apply_safety_threshold(
    text: str, 
    categories: Optional[List[str]] = None, 
    threshold: float = 0.5
) -> Dict:
    """Apply category thresholds to decide whether to allow text."""
    request: SafetyRequest = {
        "text": text,
        "categories": categories,
        "threshold": threshold
    }
    response: SafetyResponse = client.moderate(request)
    
    decision = "allow"
    if response["flagged"]:
        decision = "block"
    
    return {
        "text": response["text"],
        "decision": decision,
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