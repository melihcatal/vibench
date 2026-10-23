import boto3

from safety_client import ComprehendClient


def moderate_batch(payloads, config=None):
    config = config or {}
    client = ComprehendClient(config)
    results = []
    for payload in payloads:
        response = client.detect_toxic_content(payload['text'])
        results.append({'text': payload['text'], 'toxicity': response['toxicity']})
    return results