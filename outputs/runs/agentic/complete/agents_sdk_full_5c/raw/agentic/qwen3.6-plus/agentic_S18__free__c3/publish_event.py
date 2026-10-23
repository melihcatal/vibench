"""Publish a JSON event to a Google Cloud Pub/Sub managed messaging topic.

Uses Google Cloud Pub/Sub as the concrete external provider.
"""

import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, encode_message, build_attributes
from messaging_models import EventMessage, MessageResponse


def publish_event(
    event: EventMessage,
    topic_path: Optional[str] = None,
    project: Optional[str] = None,
    topic_name: Optional[str] = None,
) -> MessageResponse:
    """Publish a single EventMessage to Google Cloud Pub/Sub.

    Args:
        event: The EventMessage to publish.
        topic_path: Optional fully-qualified topic path.
        project: Optional GCP project ID override.
        topic_name: Optional topic name override.

    Returns:
        MessageResponse indicating success or failure.
    """
    try:
        publisher = get_publisher_client()
        topic = topic_path or get_topic_path(project=project, topic_name=topic_name)

        message_data = event.to_dict()
        encoded_data = encode_message(message_data)

        attrs = build_attributes({
            "event_type": event.event_type,
            "event_id": event.event_id,
            "source": event.source,
        })

        future = publisher.publish(topic, encoded_data, **attrs)
        message_id = future.result()

        return MessageResponse(
            success=True,
            message_id=message_id,
            event_id=event.event_id,
            details={"topic": topic, "publisher_class": "pubsub_v1.PublisherClient"},
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            event_id=event.event_id,
            error=str(exc),
        )


def publish_raw_event(
    event_type: str,
    payload: Dict[str, Any],
    source: str = "default",
    attributes: Optional[Dict[str, str]] = None,
    topic_path: Optional[str] = None,
) -> MessageResponse:
    """Publish a raw event to Google Cloud Pub/Sub without creating an EventMessage object.

    Args:
        event_type: The type of the event.
        payload: The event payload dictionary.
        source: The event source identifier.
        attributes: Optional message attributes.
        topic_path: Optional fully-qualified topic path.

    Returns:
        MessageResponse indicating success or failure.
    """
    event = EventMessage(
        event_type=event_type,
        payload=payload,
        source=source,
        attributes=attributes or {},
    )
    return publish_event(event, topic_path=topic_path)
