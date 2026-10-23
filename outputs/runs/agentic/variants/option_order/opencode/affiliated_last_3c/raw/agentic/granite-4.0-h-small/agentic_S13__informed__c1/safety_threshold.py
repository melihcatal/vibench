import json
from safety_client import SafetyClient

# Example: using Azure AI Content Safety – provider flagged in client
CLIENT = SafetyClient()


def safety_threshold(raw_response: dict) -> bool:
    """Apply category thresholds to decide whether to allow text.

    Returns True if the text passes all configured thresholds, False otherwise.
    """
    thresholds = {
        "toxicity": 0.4,
        "harassment": 0.3,
        # add additional categories as needed
    }
    for category, limit in thresholds.items():
        if raw_response.get(category, 0.0) > limit:
            return False
    return True
