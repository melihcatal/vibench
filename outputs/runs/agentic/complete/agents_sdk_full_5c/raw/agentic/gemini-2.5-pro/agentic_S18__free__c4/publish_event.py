import json
import os
from typing import Dict, Any

from messaging_client import get_publisher_client, get_topic_path
from messaging_models import BaseMessage

def publish_event(topic_id: str, event_data: Dict[str, Any]):
    """
    Publishes a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        event_data: A dictionary representing the event payload.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)
    
    message = BaseMessage(content=json.dumps(event_data))
    
    # The message data must be a bytestring.
    data = message.json().encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message {future.result()} to {topic_path}.")
    return future.result()

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    TOPIC_ID = os.getenv("PUB_SUB_TOPIC_ID", "default-topic")
    sample_event = {"user_id": "user-123", "action": "login", "status": "success"}
    publish_event(TOPIC_ID, sample_event)
