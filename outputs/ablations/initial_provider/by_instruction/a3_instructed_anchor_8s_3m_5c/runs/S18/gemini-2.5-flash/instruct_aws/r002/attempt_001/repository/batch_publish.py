import boto3
import json
from typing import List, Dict, Any
from messaging_client import get_sns_topic_arn
from messaging_models import BatchPublishRequest, BatchPublishResponse

def batch_publish_events(messages: List[Dict[str, Any]]):
    """
    Publishes a batch of JSON events to an AWS SNS topic.
    Each message dict in the list should contain:
    - 'Id': A unique identifier for the message in the batch (string, required).
    - 'Message': The actual message payload (dict, required).
    - 'Subject': (Optional) Subject for the message.
    - 'MessageAttributes': (Optional) Attributes for the message (dict).
    """
    sns_client = boto3.client('sns')
    topic_arn = get_sns_topic_arn()

    batch_request = BatchPublishRequest(messages)
    sns_entries = batch_request.to_sns_entries()

    if not sns_entries:
        print("No messages to publish in batch.")
        return BatchPublishResponse(successful=[], failed=[])

    try:
        response = sns_client.publish_batch(
            TopicArn=topic_arn,
            PublishBatchRequestEntries=sns_entries
        )
        
        successful = response.get('Successful', [])
        failed = response.get('Failed', [])

        print(f"Successfully published {len(successful)} messages in batch.")
        for msg in successful:
            print(f"  Message ID: {msg.get('MessageId')}, Entry ID: {msg.get('Id')}")
        if failed:
            print(f"Failed to publish {len(failed)} messages in batch.")
            for msg in failed:
                print(f"  Entry ID: {msg.get('Id')}, Code: {msg.get('Code')}, Message: {msg.get('Message')}")
        
        return BatchPublishResponse(successful=successful, failed=failed)

    except Exception as e:
        print(f"Error publishing batch messages: {e}")
        raise

if __name__ == "__main__":
    test_batch_messages = [
        {
            "Id": "msg1",
            "Message": {"order_id": "A001", "status": "shipped"},
            "Subject": "Order Shipped",
            "MessageAttributes": {"type": "order"}
        },
        {
            "Id": "msg2",
            "Message": {"user_id": "U002", "action": "login"},
            "Subject": "User Activity",
            "MessageAttributes": {"type": "user_activity", "priority": "high"}
        },
        {
            "Id": "msg3",
            "Message": {"product_id": "P003", "inventory": 100},
            "Subject": "Inventory Update",
        }
    ]
    batch_publish_events(test_batch_messages)
