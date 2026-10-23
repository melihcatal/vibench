import boto3
import json
import os
from typing import List, Dict
from messaging_client import get_sns_client

def batch_publish_events(topic_arn: str, events: List[Dict]) -> dict:
    """Publishes a batch of JSON events to an AWS SNS topic.

    Args:
        topic_arn: The ARN of the SNS topic.
        events: A list of dictionaries, where each dictionary represents a JSON event.
                Each event dict must have an 'Id' key (string) for batching.

    Returns:
        A dictionary containing the response from the SNS publish_batch operation.
    """
    sns_client = get_sns_client()
    
    # Prepare entries for publish_batch
    # Each entry must have 'Id', 'Message', 'MessageStructure'
    entries = []
    for i, event_data in enumerate(events):
        # Ensure each event has an 'Id' for batch publishing.
        # If not provided, generate a simple one. SNS requires a unique Id per entry.
        entry_id = event_data.get('Id') or f"msg-{i}-{os.urandom(4).hex()}"
        
        entries.append({
            'Id': entry_id,
            'Message': json.dumps(event_data),
            'MessageStructure': 'json'
        })
    
    if not entries:
        return {"Failed": [], "Successful": []}

    try:
        response = sns_client.publish_batch(
            TopicArn=topic_arn,
            PublishBatchRequestEntries=entries
        )
        return response
    except Exception as e:
        print(f"Error publishing batch events to SNS: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and a configured SNS topic)
    # Ensure AWS_REGION environment variable is set.
    # export AWS_REGION="us-east-1"
    # export SNS_TOPIC_ARN="arn:aws:sns:us-east-1:123456789012:MyEventTopic"

    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:ExampleTopic")
    sample_events = [
        {
            "Id": "event-001",
            "type": "user_registered",
            "data": {"user_id": "U001", "username": "alice"}
        },
        {
            "Id": "event-002",
            "type": "product_viewed",
            "data": {"user_id": "U002", "product_id": "P005"}
        },
        {
            "Id": "event-003",
            "type": "cart_updated",
            "data": {"user_id": "U001", "item_count": 3}
        }
    ]

    print(f"Publishing batch of {len(sample_events)} events to {sns_topic_arn}")
    for event in sample_events:
        print(f" - {json.dumps(event)}")

    try:
        batch_publish_response = batch_publish_events(sns_topic_arn, sample_events)
        print(f"Batch publish successful: {batch_publish_response}")
    except Exception as e:
        print(f"Failed to batch publish: {e}")
