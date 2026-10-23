import json
import os
from messaging_client import AWSMessagingClient
from messaging_models import EventMessage


def publish_event(event: EventMessage, topic_arn: str) -> dict:
    """Publishes a JSON event to an AWS SNS topic."""
    sns_client = AWSMessagingClient().get_sns_client()
    try:
        message_attributes = {
            key: {"DataType": "String", "StringValue": value}
            for key, value in event.attributes.items()
        }
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(event.data),
            MessageAttributes=message_attributes,
        )
        return {"status": "success", "message_id": response["MessageId"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Example Usage (replace with actual topic ARN and event data)
    sns_topic_arn = os.environ.get(
        "AWS_SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:MyTestTopic"
    )
    sample_event = EventMessage(
        id="msg123",
        type="order_created",
        data={
            "order_id": "ORD-001",
            "customer_id": "CUST-001",
            "items": [{"product_id": "PROD-001", "quantity": 2}],
        },
        attributes={"source": "web_app", "priority": "high"},
    )

    result = publish_event(sample_event, sns_topic_arn)
    print(result)
