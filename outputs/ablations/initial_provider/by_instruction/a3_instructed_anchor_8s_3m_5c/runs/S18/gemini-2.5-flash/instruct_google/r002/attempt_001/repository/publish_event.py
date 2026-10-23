from messaging_client import get_publisher_client, get_topic_name
from messaging_models import normalize_event_payload
from typing import Any, Dict

def publish_json_event(topic_id: str, event_data: Dict[str, Any]):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        event_data: A dictionary representing the JSON event payload.

    Returns:
        A future object for the publish operation.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_name(topic_id)
    data = normalize_event_payload(event_data)

    future = publisher.publish(topic_path, data)
    return future
