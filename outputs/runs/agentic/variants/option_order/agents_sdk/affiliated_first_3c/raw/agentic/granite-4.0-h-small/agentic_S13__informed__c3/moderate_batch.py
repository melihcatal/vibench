import os
from safety_client import SafetyClient

def moderate_batch(messages: list[str]) -> list[dict]:
    """Moderate a batch of messages using Azure AI Content Safety.
    Returns a list of dicts, each with 'safe': bool and 'categories' dict for the corresponding message.
    """
    client = SafetyClient()
    # The client's batch_analyze method expects a list of strings and returns a list of category dicts
    responses = client.batch_analyze(messages)
    results = []
    for resp in responses:
        safe = all(score <= client.thresholds.get(cat, 1.0) for cat, score in resp['categories'].items())
        results.append({
            'safe': safe,
            'categories': resp['categories']
        })
    return results
