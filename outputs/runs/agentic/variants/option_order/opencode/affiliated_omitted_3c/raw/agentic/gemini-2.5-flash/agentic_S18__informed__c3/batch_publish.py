import json
import os
from typing import List
from messaging_client import AWSMessagingClient
from messaging_models import BatchEventMessage


def batch_publish(messages: List[BatchEventMessage], topic_arn: str) -> dict:
    """Publishes a batch of messages to an AWS SNS topic."""
    sns_client = AWSMessagingClient().get_sns_client()
    entries = []
    for msg in messages:
        entry = {
            "Id": msg.id,
            "Message": msg.message_body,
            "MessageAttributes": {
                key: {"DataType": "String", "StringValue": value}
                for key, value in msg.message_attributes.items()
            },
        }
        entries.append(entry)

    if not entries:
        return {
            "status": "warning",
            "message": "No messages to publish.",
            "published_messages": [],
        }

    try:
        # SNS PublishBatch supports up to 10 messages
        response = sns_client.publish_batch(
            TopicArn=topic_arn, PublishBatchRequestEntries=entries
        )
        successful = response.get("Successful", [])
        failed = response.get("Failed", [])
        return {
            "status": "success" if not failed else "partial_failure",
            "message": f"Published {len(successful)} messages. {len(failed)} failed.",
            "successful_messages": successful,
            "failed_messages": failed,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Example Usage (replace with actual topic ARN and event data)
    sns_topic_arn = os.environ.get(
        "AWS_SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:MyTestTopic"
    )

    sample_messages = [
        BatchEventMessage(
            id="batch-msg-001",
            message_body=json.dumps({"event": "user_registered", "user_id": "U001"}),
            message_attributes={"source": "auth_service", "environment": "dev"},
        ),
        BatchEventMessage(
            id="batch-msg-002",
            message_body=json.dumps({"event": "product_viewed", "product_id": "P005"}),
            message_attributes={"source": "frontend", "user_agent": "chrome"},
        ),
    ]

    print(f"Attempting to publish batch messages to {sns_topic_arn}...")
    result = batch_publish(sample_messages, sns_topic_arn)
    print(result)
