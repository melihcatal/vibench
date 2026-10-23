import json
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_project_id, DEAD_LETTER_TOPIC_ID
from messaging_models import EventPayload


def send_to_dead_letter(payload: EventPayload, reason: str):
    """Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GCP project ID not set.")

    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, DEAD_LETTER_TOPIC_ID)

    data = json.dumps(payload).encode("utf-8")

    future = publisher.publish(topic_path, data, failure_reason=reason)
    return future.result()
