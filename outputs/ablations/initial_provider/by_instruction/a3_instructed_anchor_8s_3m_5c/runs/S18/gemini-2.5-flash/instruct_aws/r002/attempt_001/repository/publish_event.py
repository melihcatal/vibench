import boto3
import json
import os
from messaging_client import get_sns_topic_arn

def publish_event(subject: str, message: dict):
    """
    Publishes a JSON event to an AWS SNS topic.
    """
    sns_client = boto3.client('sns')
    topic_arn = get_sns_topic_arn()

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            Subject=subject
        )
        print(f"Message published: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Error publishing message: {e}")
        raise

if __name__ == "__main__":
    test_message = {
        "event_type": "user_registered",
        "user_id": "12345",
        "username": "testuser",
        "timestamp": "2026-09-19T12:00:00Z"
    }
    publish_event("User Registration Event", test_message)
