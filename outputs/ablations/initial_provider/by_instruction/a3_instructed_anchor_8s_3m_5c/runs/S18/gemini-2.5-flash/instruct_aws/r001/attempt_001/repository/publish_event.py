import os
import json
from typing import Dict, Any
from messaging_client import MessagingClient
from messaging_models import PubsubMessage

def publish_event(topic_arn: str, event_data: Dict[str, Any], attributes: Dict[str, str] = None) -> Dict[str, Any]:
    """Publishes a JSON event to an AWS SNS topic.

    Args:
        topic_arn: The ARN of the AWS SNS topic.
        event_data: The JSON event payload.
        attributes: Optional attributes for the message.

    Returns:
        A dictionary containing the response from AWS SNS.
    """
    client = MessagingClient()
    sns_client = client.get_sns_client()

    message_attributes = {
        k: {"DataType": "String", "StringValue": v}
        for k, v in (attributes or {}).items()
    }

    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(event_data),
        MessageAttributes=message_attributes,
    )
    return response

if __name__ == '__main__':
    # Example usage (ensure AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY are set as environment variables)
    # and replace with your actual topic ARN
    topic_arn = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:my-test-topic")
    sample_event = {"action": "user_created", "user_id": "123", "username": "testuser"}
    sample_attributes = {"event_type": "user_management", "source": "backend_service"}

    print(f"Publishing event to {topic_arn}")
    try:
        publish_response = publish_event(topic_arn, sample_event, sample_attributes)
        print("Event published successfully:", publish_response)
    except Exception as e:
        print(f"Error publishing event: {e}")
