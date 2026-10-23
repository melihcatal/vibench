import json
from typing import List, Dict, Any
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def publish_batch_events(topic_name: str, events: List[Dict[str, Any]]) -> List[str]:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic.

    Args:
        topic_name: The name of the Pub/Sub topic.
        events: A list of dictionaries, where each dictionary is a JSON event payload.
                Each event can optionally include an 'attributes' key with a dictionary of string attributes.

    Returns:
        A list of message IDs for the published messages.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_name)

    futures = []
    for event_data in events:
        attributes = event_data.pop("attributes", {})
        message = PubSubMessage(event_data, attributes=attributes)
        data_bytes = message.to_json()
        futures.append(publisher.publish(topic_path, data_bytes, **message.attributes))

    # Wait for all the publish futures to resolve
    message_ids = [future.result() for future in futures]
    return message_ids
