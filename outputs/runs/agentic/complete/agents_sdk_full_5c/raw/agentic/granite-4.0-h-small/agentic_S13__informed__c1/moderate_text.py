# moderate_text.py
import json
import os
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_text(user_text: str) -> ModerationResponse:
    """Score a single user message for policy‑violating content.

    Uses Amazon Comprehend Toxicity as the concrete provider.
    """
    client = SafetyClient()
    request = ModerationRequest(
        text=user_text,
        language=client.detect_language(user_text),
    )
    response = client.detect_toxicity(request)
    return response

if __name__ == "__main__":
    sample = "I hate you!"
    result = moderate_text(sample)
    print(json.dumps(result.to_dict(), indent=2))
