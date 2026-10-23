import boto3

from safety_client import ComprehendClient


def moderation_summary(payloads, config=None):
    config = config or {}
    client = ComprehendClient(config)
    results = []
    for payload in payloads:
        response = client.detect_toxic_content(payload['text'])
        results.append({'text': payload['text'], 'toxicity': response['toxicity']})
    summary = {'total_messages': len(payloads), 'toxic_messages': sum(1 for result in results if result['toxicity'] > 0.5)}
    return summary