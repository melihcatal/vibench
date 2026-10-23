"""
[SAME-SCENARIO] Publish a JSON event to Google Cloud Pub/Sub managed messaging topic.
Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
from messaging_models import PubSubEvent, PublishResult
from messaging_client import get_pubsub_publisher_client, get_topic_path, publish_with_retry


def publish_event(
    event: PubSubEvent,
    topic_id: str = None,
    project_id: str = None,
) -> PublishResult:
    """
    Publish a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event: The PubSubEvent to publish.
        topic_id: The Pub/Sub topic identifier.
        project_id: The GCP project ID.

    Returns:
        PublishResult with message ID and status.
    """
    topic_id = topic_id or os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
    publisher = get_pubsub_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    message_bytes = event.to_json().encode("utf-8")

    attributes = {
        "event_type": event.event_type,
        "source": event.source,
        "event_id": event.event_id,
    }
    attributes.update(event.attributes)

    message_id = publish_with_retry(publisher, topic_path, message_bytes, attributes)

    return PublishResult(
        message_id=message_id,
        status="published",
        topic=topic_path,
    )
