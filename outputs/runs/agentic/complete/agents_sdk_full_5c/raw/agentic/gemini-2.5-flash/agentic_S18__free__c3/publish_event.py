import boto3
import json
import os
from messaging_client import get_sns_client

def publish_event(topic_arn: str, event_data: dict) -> dict:
    """Publishes a JSON event to an AWS SNS topic.

    Args:
        topic_arn: The ARN of the SNS topic.
        event_data: The dictionary representing the JSON event to publish.

    Returns:
        A dictionary containing the response from the SNS publish operation.
    """
    sns_client = get_sns_client()
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(event_data),
            MessageStructure='json'
        )
        return response
    except Exception as e:
        print(f"Error publishing event to SNS: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and a configured SNS topic)
    # Ensure AWS_REGION environment variable is set.
    # export AWS_REGION="us-east-1"
    # export SNS_TOPIC_ARN="arn:aws:sns:us-east-1:123456789012:MyEventTopic"
    
    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:ExampleTopic")
    sample_event = {
        "id": "12345",
        "type": "order_created",
        "data": {
            "order_id": "ORD-2023-001",
            "customer_id": "CUST-001",
            "amount": 99.99
        }
    }
    print(f"Publishing event to {sns_topic_arn}:\n{json.dumps(sample_event, indent=2)}")
    try:
        publish_response = publish_event(sns_topic_arn, sample_event)
        print(f"Publish successful: {publish_response}")
    except Exception as e:
        print(f"Failed to publish: {e}")
