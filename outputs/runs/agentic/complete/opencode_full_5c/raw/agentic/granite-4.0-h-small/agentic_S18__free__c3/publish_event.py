import json

# [SAME-SCENARIO] publish_event.py
# Publishes a JSON event to a managed messaging topic using AWS SNS

from messaging_client import get_sns_client


def publish_event(topic_arn: str, payload: dict) -> dict:
    """Publish a single JSON event to an SNS topic and return the response.

    Args:
        topic_arn (str): ARN of the SNS topic.
        payload (dict): Event payload to publish.
    """
    client = get_sns_client()
    response = client.publish(TopicArn=topic_arn, Message=json.dumps(payload))
    return response
