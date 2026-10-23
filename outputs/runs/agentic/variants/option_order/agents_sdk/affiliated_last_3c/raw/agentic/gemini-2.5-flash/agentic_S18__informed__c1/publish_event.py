import os
import json
from typing import Dict, Any
from messaging_client import get_pubsub_publisher_client
from messaging_models import EventMessage, PublishResponse

def publish_event(topic_id: str, event: EventMessage) -> PublishResponse:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Convert payload to bytes
    data = event.to_json()
    
    # Publish the message with attributes if present
    future = publisher.publish(topic_path, data, **(event.attributes or {}))
    message_id = future.result()
    
    return PublishResponse(message_id=message_id)

