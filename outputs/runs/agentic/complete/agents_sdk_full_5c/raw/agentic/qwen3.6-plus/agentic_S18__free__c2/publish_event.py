"""Publish a JSON event to Google Cloud Pub/Sub managed messaging topic."""

import json
import uuid
from datetime import datetime, timezone

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.publisher.types import PublishRequest

from messaging_client import get_pubsub_publisher_client, get_pubsub_config
from messaging_models import EventMessage, PublishResponse


def publish_event(event: EventMessage, topic_id: str) -> PublishResponse:
    """Publish a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event: EventMessage object containing event data and metadata.
        topic_id: Google Cloud Pub/Sub topic name (without the full path).

    Returns:
        PublishResponse with message ID and publish metadata.
    """
    config = get_pubsub_config()
    project_id = config["project_id"]

    publisher_client = get_pubsub_publisher_client()
    topic_path = publisher_client.topic_path(project_id, topic_id)

    payload = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "source": event.source,
        "payload": event.payload,
        "metadata": event.metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    message_body = json.dumps(payload).encode("utf-8")

    attributes = {
        "event_type": event.event_type,
        "source": event.source,
        "event_id": event.event_id,
        "content_type": "application/json",
    }

    future = publisher_client.publish(
        topic_path, data=message_body, **attributes
    )
    message_id = future.result()

    return PublishResponse(
        message_id=message_id,
        event_id=event.event_id,
        topic_path=topic_path,
        status="published",
    )


def publish_event_from_dict(event_dict: dict, topic_id: str) -> PublishResponse:
    """Publish an event from a dictionary to Google Cloud Pub/Sub.

    Args:
        event_dict: Dictionary with event fields.
        topic_id: Google Cloud Pub/Sub topic name.

    Returns:
        PublishResponse with publish confirmation.
    """
    event = EventMessage(
        event_id=event_dict.get("event_id", str(uuid.uuid4())),
        event_type=event_dict.get("event_type", "custom"),
        source=event_dict.get("source", "api"),
        payload=event_dict.get("payload", {}),
        metadata=event_dict.get("metadata", {}),
    )
    return publish_event(event, topic_id)
