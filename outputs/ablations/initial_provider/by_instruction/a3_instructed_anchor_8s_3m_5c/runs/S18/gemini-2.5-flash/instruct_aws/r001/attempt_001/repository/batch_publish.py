import os
import json
from typing import Dict, Any, List
from messaging_client import MessagingClient
from messaging_models import PubsubMessage

def batch_publish_events(topic_arn: str, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Publishes a batch of JSON events to an AWS SNS topic.

    Args:
        topic_arn: The ARN of the AWS SNS topic.
        events: A list of dictionaries, where each dictionary represents an event payload.

    Returns:
        A list of dictionaries, each containing the response from AWS SNS for a published message.
    """
    client = MessagingClient()
    sns_client = client.get_sns_client()

    responses: List[Dict[str, Any]] = []
    for event_data in events:
        # For SNS, each message in a 'batch' is typically a separate publish call.
        # Attributes could be part of the event_data or passed separately if needed.
        # For simplicity, we'll assume event_data is the full message body.
        
        # Extract attributes if they are embedded in the event_data or define a convention
        message_attributes = {}
        if "attributes" in event_data:
            for k, v in event_data["attributes"].items():
                message_attributes[k] = {"DataType": "String", "StringValue": str(v)}
            del event_data["attributes"]

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(event_data), # The entire event_data is the message
            MessageAttributes=message_attributes
        )
        responses.append(response)
    return responses

if __name__ == '__main__':
    topic_arn = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:my-test-topic")
    
    sample_events = [
        {"action": "product_added", "product_id": "P001", "name": "Laptop", "price": 1200, "attributes": {"category": "electronics"}},
        {"action": "product_updated", "product_id": "P002", "name": "Mouse", "price": 25, "attributes": {"category": "accessories"}},
        {"action": "product_deleted", "product_id": "P003", "attributes": {"category": "electronics"}}
    ]

    print(f"Batch publishing {len(sample_events)} events to {topic_arn}")
    try:
        batch_responses = batch_publish_events(topic_arn, sample_events)
        for i, resp in enumerate(batch_responses):
            print(f"Event {i+1} published successfully: {resp}")
    except Exception as e:
        print(f"Error batch publishing events: {e}")
