from messaging_client import get_publisher_client, get_topic_name
from messaging_models import normalize_event_payload
from typing import Any, Dict, List

def publish_batch_events(topic_id: str, event_data_list: List[Dict[str, Any]]):
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        event_data_list: A list of dictionaries, each representing a JSON event payload.

    Returns:
        A list of future objects for the publish operations.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_name(topic_id)

    futures = []
    for event_data in event_data_list:
        data = normalize_event_payload(event_data)
        future = publisher.publish(topic_path, data)
        futures.append(future)

    return futures
