# batch_publish.py
# SAME-SCENARIO: Publish a batch of JSON events to Amazon SNS topic

import os
import json
import boto3

session = boto3.Session()
sns_client = session.client("sns")


def batch_publish(topic_arn, messages):
    """Publish multiple messages as separate SNS publishes.

    Args:
        topic_arn (str): ARN of the SNS topic.
        messages (list[dict]): List of JSON-serializable payloads.
    """
    for idx, payload in enumerate(messages, start=1):
        message_id = f"batch-msg-{idx}"
        sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(payload),
            MessageAttributes={
                "batchId": {"DataType": "String", "StringValue": topic_arn},
                "msgId": {"DataType": "String", "StringValue": message_id},
            },
        )
    print(f"Published {len(messages)} messages to topic {topic_arn}.")


if __name__ == "__main__":
    # Example usage: read environment variables for topic and batch data
    topic = os.getenv("BATCH_PUBLISH_TOPIC_ARN")
    if not topic:
        raise RuntimeError("Set BATCH_PUBLISH_TOPIC_ARN environment variable")
    sample_batch = [
        {"eventId": "b1", "msg": "Batch message 1", "ts": "2025-08-01T12:00:00Z"},
        {"eventId": "b2", "msg": "Batch message 2", "ts": "2025-08-01T12:01:00Z"},
        {"eventId": "b3", "msg": "Batch message 3", "ts": "2025-08-01T12:02:00Z"},
    ]
    batch_publish(topic, sample_batch)
