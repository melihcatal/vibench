
import os
import json
import boto3

def publish_event(topic_arn: str, event_data: dict, region_name: str = None):
    """
    Publishes a JSON event to an AWS SNS topic.

    Args:
        topic_arn: The ARN of the SNS topic.
        event_data: The JSON data to publish.
        region_name: The AWS region (e.g., "us-east-1"). If None, boto3 will use the default configured region.
    """
    try:
        if region_name:
            sns_client = boto3.client("sns", region_name=region_name)
        else:
            sns_client = boto3.client("sns")

        message = json.dumps(event_data)

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='json' # This tells SNS to interpret the message as a JSON payload
        )

        print(f"Event published successfully to topic {topic_arn}. MessageId: {response['MessageId']}")
        return response

    except Exception as e:
        print(f"Error publishing event to SNS: {e}")
        raise

if __name__ == "__main__":
    # Example Usage:
    # Set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SNS_TOPIC_ARN
    # For local testing, you might set these in your shell or use a tool like python-dotenv

    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # Default to us-east-1 if not specified

    if not sns_topic_arn:
        print("Error: SNS_TOPIC_ARN environment variable not set.")
        exit(1)

    sample_event = {
        "eventType": "UserRegistered",
        "userId": "12345",
        "timestamp": "2026-09-20T10:00:00Z",
        "details": {
            "email": "user@example.com",
            "username": "testuser"
        }
    }

    print(f"Attempting to publish event to SNS Topic: {sns_topic_arn} in region {aws_region}")
    publish_event(sns_topic_arn, sample_event, aws_region)
