# Applies category thresholds to decide whether to allow text using Azure AI Content Safety

from typing import Dict
from safety_client import AzureContentSafetyClient
from safety_models import SafetyCategory, TextModerationRequest, SafetyDecision


def apply_safety_threshold(
    text: str, 
    threshold_overrides: Dict[SafetyCategory, float]
) -> bool:
    """Apply category thresholds to decide if text is allowed using Azure AI Content Safety."""
    client = AzureContentSafetyClient()
    request: TextModerationRequest = {
        "text": text,
        "categories": list(threshold_overrides.keys()),
        "threshold_overrides": threshold_overrides,
    }
    response = client.moderate_text(request)
    return not any(decision["flagged"] for decision in response["decisions"])