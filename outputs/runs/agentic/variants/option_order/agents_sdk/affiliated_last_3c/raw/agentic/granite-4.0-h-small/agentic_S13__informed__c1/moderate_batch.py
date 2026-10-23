import os
from safety_client import SafetyClient

def moderate_batch(messages: list[str]) -> list[dict]:
    """Moderate a list of messages using the safety provider.

    Provider: Amazon Comprehend Toxicity (AWS Comprehend) via boto3.
    """
    client = SafetyClient()
    responses = client.detect_toxicity_batch(texts=messages)
    return [
        {
            "status": r.get('status'),
            "labels": r.get('labels'),
            "confidence": r.get('confidence')
        }
        for r in responses
    ]
