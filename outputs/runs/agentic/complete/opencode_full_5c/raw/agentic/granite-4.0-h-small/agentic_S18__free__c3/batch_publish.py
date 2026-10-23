import json

# [SAME-SCENARIO] batch_publish.py
# Publishes a batch of messages (up to 10) to an SNS topic

from messaging_client import get_sns_client


def batch_publish(topic_arn: str, messages: list[dict]) -> list[dict]:
    """Publish a batch of messages (max 10) to an SNS topic.

    Args:
        topic_arn (str): SNS topic ARN.
        messages (list[dict]): List of payloads to send.
    Returns:
        list[dict]: Responses for each publish call.
    Raises:
        ValueError: If more than 10 messages are provided.
    """
    if len(messages) > 10:
        raise ValueError("SNS batch publish limited to 10 messages")
    client = get_sns_client()
    responses = []
    for payload in messages:
        resp = client.publish(TopicArn=topic_arn, Message=json.dumps(payload))
        responses.append(resp)
    return responses
