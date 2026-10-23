import boto3

from safety_client import ComprehendClient


def redact_unsafe(payload, config=None):
    config = config or {}
    client = ComprehendClient(config)
    response = client.detect_toxic_content(payload['text'])
    if response['toxicity'] > 0.5:
        redacted_text = ''.join(['*' if char.isalnum() else char for char in payload['text']])
        return {'redacted_text': redacted_text}
    else:
        return {'original_text': payload['text']}