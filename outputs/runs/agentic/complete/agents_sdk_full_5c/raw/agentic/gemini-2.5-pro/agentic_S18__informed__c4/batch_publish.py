import os
import json
import uuid
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import Event

def publish_batch(events: list[Event]):
    """Publishes a batch of events to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    topic_id = os.getenv("GCP_PUBSUB_TOPIC_ID", "my-topic")

    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, project_id, topic_id)
    
    publish_futures = []

    for event in events:
        data = event.to_json().encode("utf-8")
        future = publisher.publish(
            topic_path, data, event_id=event.event_id
        )
        publish_futures.append(future)

    try:
        results = [future.result(timeout=30) for future in publish_futures]
        print(f"Published {len(results)} messages in a batch.")
        return results
    except TimeoutError:
        print("Timeout while waiting for messages to publish.")
        return []
