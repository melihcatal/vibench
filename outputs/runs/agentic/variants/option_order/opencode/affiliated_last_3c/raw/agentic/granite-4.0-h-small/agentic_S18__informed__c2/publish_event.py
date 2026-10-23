# publish_event.py
# SAME-SCENARIO: Publish a JSON event to Amazon SNS topic

import os
import json
import boto3

# Use AWS credentials from environment
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY should be set

session = boto3.Session()
sns_client = session.client("sns")


def publish_event(topic_arn, payload_json):
    """Publish a JSON payload as an SNS message to the specified topic ARN.

    Args:
        topic_arn (str): The ARN of the SNS topic.
        payload_json (dict): JSON-serializable payload.
    """
    response = sns_client.publish(TopicArn=topic_arn, Message=json.dumps(payload_json))
    print(f"Message published. SNS MessageId: {response['MessageId']}")


if __name__ == "__main__":
    # Example usage: read topic ARN and payload from env vars
    topic = os.getenv("PUBLISH_TOPIC_ARN")
    if not topic:
        raise RuntimeError("Set PUBLISH_TOPIC_ARN environment variable")
    sample_payload = {
        "eventId": "example-123",
        "msg": "Hello from publish_event.py",
        "timestamp": "2025-08-01T12:00:00Z",
    }
    publish_event(topic, sample_payload)
