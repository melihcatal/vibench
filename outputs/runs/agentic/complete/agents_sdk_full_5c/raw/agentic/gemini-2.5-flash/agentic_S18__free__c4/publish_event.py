import os
import json
import boto3

def publish_event(topic_arn: str, event_data: dict) -> dict:
    """Publishes a JSON event to an AWS SNS topic."""
    sns_client = boto3.client(
        "sns",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(event_data),
            MessageStructure='json'
        )
        return {"message_id": response["MessageId"], "status": "success"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION and SNS_TOPIC_ARN environment variables)
    # Ensure AWS credentials are configured
    # topic_arn = os.environ.get("SNS_TOPIC_ARN")
    # if not topic_arn:
    #     print("SNS_TOPIC_ARN environment variable not set.")
    # else:
    #     event = {"type": "user_registered", "user_id": "123", "email": "test@example.com"}
    #     result = publish_event(topic_arn, event)
    #     print(f"Publish result: {result}")
    pass
