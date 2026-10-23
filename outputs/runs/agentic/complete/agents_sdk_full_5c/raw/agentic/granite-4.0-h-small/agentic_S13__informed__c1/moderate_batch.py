# moderate_batch.py
import json
import os
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_batch(messages: list[str]) -> list[ModerationResponse]:
    """Moderate a list of messages and return per‑message decisions.

    Uses Amazon Comprehend Toxicity as the concrete provider.
    """
    client = SafetyClient()
    batch = [ModerationRequest(text=txt, language=client.detect_language(txt)) for txt in messages]
    responses = client.batch_detect_toxicity(batch)
    return responses

if __name__ == "__main__":
    msgs = [
        "You are useless.",
        "This is a friendly note.",
        "I will bomb the place."
    ]
    results = moderate_batch(msgs)
    print(json.dumps([r.to_dict() for r in results], indent=2))
