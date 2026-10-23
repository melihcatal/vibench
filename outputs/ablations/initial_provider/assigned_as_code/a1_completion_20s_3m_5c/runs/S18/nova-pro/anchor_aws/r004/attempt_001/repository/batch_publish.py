import boto3

from messaging_client import get_sns_client


def batch_publish(payloads, config=None):
    config = config or {}
    client = get_sns_client()
    for payload in payloads:
        client.publish(TopicArn=config['topic_arn'], Message=json.dumps(payload))
    return {'status': 'success'}