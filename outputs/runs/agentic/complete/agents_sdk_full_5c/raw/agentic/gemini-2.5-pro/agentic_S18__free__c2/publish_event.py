import json
from typing import Optional

from messaging_client import get_publisher_client, get_topic_path, MAIN_TOPIC_ID
from messaging_models import EventPayload

def publish_event(event: EventPayload) -> Optional[str]:
    """
    Publishes a single JSON event to a Google Cloud Pub/Sub topic.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(MAIN_TOPIC_ID)
    
    data = event.to_json().encode("utf-8")
    
    future = publisher.publish(topic_path, data, correlation_id=event.event_id)
    
    try:
        message_id = future.result()
        print(f"Published message with ID: {message_id} to {topic_path}")
        return message_id
    except Exception as e:
        print(f"An error occurred while publishing message: {e}")
        return None
