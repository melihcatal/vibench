from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage
import json
from typing import List, Dict, Any, Tuple


def batch_publish_events(topic_id: str, events: List[Dict[str, Any]]) -> List[str]:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        events: A list of dictionaries, where each dictionary is an event payload.
                Each event can optionally contain a '_attributes' key for message attributes.

    Returns:
        A list of message IDs for the published messages.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for event_data in events:
        attributes = event_data.pop("_attributes", {})  # Extract attributes if present
        message = PubSubMessage(event_data, attributes=attributes)
        data = message.to_json().encode("utf-8")
        futures.append(publisher.publish(topic_path, data, **attributes))

    return [future.result() for future in futures]
