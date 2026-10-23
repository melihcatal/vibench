import os
import json
from typing import List
from messaging_client import get_pubsub_publisher_client
from messaging_models import EventMessage, PublishResponse, BatchPublishRequest

def batch_publish(topic_id: str, batch_request: BatchPublishRequest) -> List[PublishResponse]:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for event in batch_request.messages:
        data = event.to_json()
        future = publisher.publish(topic_path, data, **(event.attributes or {}))
        futures.append(future)

    # Wait for all messages to be published and collect their IDs
    results = [PublishResponse(message_id=future.result()) for future in futures]
    
    return results
