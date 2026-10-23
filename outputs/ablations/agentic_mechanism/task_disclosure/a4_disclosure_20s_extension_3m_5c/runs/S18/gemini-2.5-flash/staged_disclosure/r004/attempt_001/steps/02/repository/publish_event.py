import boto3
import json
import os

def publish_event_to_sns(topic_arn: str, event_data: dict):
    """
    Publishes a JSON event to an AWS SNS topic.

    Args:
        topic_arn: The ARN of the SNS topic.
        event_data: The JSON event data as a dictionary.
    """
    sns_client = boto3.client(
        'sns',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),  # Use environment variable or default
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    message = json.dumps(event_data)

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='string'
        )
        print(f"Message published to SNS topic: {topic_arn}")
        print(f"Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error publishing message to SNS: {e}")

if __name__ == "__main__":
    # Replace with your actual SNS topic ARN
    # You can also set this as an environment variable: export SNS_TOPIC_ARN="arn:aws:sns:..."
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:123456789012:MyTestTopic')

    # Example JSON event data
    event = {
        "event_type": "user_registered",
        "user_id": "12345",
        "timestamp": "2023-10-27T10:00:00Z",
        "details": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    }

    if sns_topic_arn == 'arn:aws:sns:us-east-1:123456789012:MyTestTopic':
        print("WARNING: Using a placeholder SNS topic ARN. Please update 'sns_topic_arn' or set the 'SNS_TOPIC_ARN' environment variable.")
        print("Example: export SNS_TOPIC_ARN="arn:aws:sns:your-region:your-account-id:your-topic-name"")

    publish_event_to_sns(sns_topic_arn, event)
