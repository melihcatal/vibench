import boto3
import json
import os

def publish_event_to_sns(topic_arn: str, event_data: dict, region_name: str = 'us-east-1'):
    """
    Publishes a JSON event to an AWS SNS topic.

    Args:
        topic_arn (str): The Amazon Resource Name (ARN) of the SNS topic.
        event_data (dict): The event data as a dictionary, which will be converted to JSON.
        region_name (str): The AWS region where the SNS topic is located.
    """
    try:
        # AWS SDK client for SNS
        sns_client = boto3.client('sns', region_name=region_name)

        # Convert the event data dictionary to a JSON string
        message = json.dumps(event_data)

        # Publish the message to the SNS topic
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='string'
        )

        print(f"Event published successfully! Message ID: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Error publishing event to SNS: {e}")
        raise

if __name__ == "__main__":
    # --- Configuration ---
    # Replace with your actual SNS Topic ARN
    # You can set this as an environment variable or directly in the code
    SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:your-aws-region:123456789012:your-topic-name")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

    # Example event data
    example_event = {
        "event_type": "user_registered",
        "user_id": "12345",
        "timestamp": "2026-09-20T10:00:00Z",
        "details": {
            "email": "test@example.com",
            "signup_method": "web"
        }
    }

    if "your-aws-region" in SNS_TOPIC_ARN or "123456789012" in SNS_TOPIC_ARN or "your-topic-name" in SNS_TOPIC_ARN:
        print("WARNING: Please update SNS_TOPIC_ARN and AWS_REGION with your actual AWS SNS topic details.")
        print("To run this example, set the SNS_TOPIC_ARN environment variable or modify the script.")
    else:
        print(f"Attempting to publish event to SNS Topic: {SNS_TOPIC_ARN} in region {AWS_REGION}")
        publish_event_to_sns(SNS_TOPIC_ARN, example_event, AWS_REGION)
