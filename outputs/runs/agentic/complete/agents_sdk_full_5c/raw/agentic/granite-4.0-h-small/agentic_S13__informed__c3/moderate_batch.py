import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

def moderate_batch(batch: List[str]) -> List[dict]:
    """Score a batch of texts for unsafe content using Azure AI Content Safety.
    Returns a list of dicts, each matching the format of moderate_text().
    """
    client = SafetyClient()
    results = []
    for text in batch:
        payload = SafetyModels.build_payload(text)
        raw = client.detect(text)
        normalized = SafetyModels.normalize_response(raw)
        results.append({
            "provider": "Azure",
            "raw": raw,
            "normalized": normalized,
            "is_safe": normalized['result'] == "safe"
        })
    return results

if __name__ == "__main__":
    sample = ["Hello, how are you?", "This is a bad message."]
    print(moderate_batch(sample))
