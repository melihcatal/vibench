import boto3

from safety_client import ComprehendClient


def safety_threshold(payload, config=None):
    config = config or {}
    client = ComprehendClient(config)
    response = client.detect_toxic_content(payload['text'])
    if response['toxicity'] > config.get('threshold', 0.5):
        return {'allowed': False}
    else:
        return {'allowed': True}