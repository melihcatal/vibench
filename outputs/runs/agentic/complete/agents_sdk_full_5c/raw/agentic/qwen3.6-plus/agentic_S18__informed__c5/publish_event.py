"""Publish a JSON event to Google Cloud Pub/Sub managed messaging topic.

Uses the google-cloud-pubsub SDK to publish a single event with
attributes to a configured topic. Authentication relies on
GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import (
    get_publisher,
    topic_path,
    normalize_payload,
    build_attributes,
)
from messaging_models import PublishRequest, PublishResponse


def publish_event(
    event_type: str,
    source: str,
    payload: Dict[str, Any],
    event_id: Optional[str] = None,
    extra_attributes: Optional[Dict[str, str]] = None,
    topic_id_override: Optional[str] = None,
) -> PublishResponse:
    """Publish a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event_type: Type identifier for the event (e.g. "order.created").
        source: Origin system or service name.
        payload: Dictionary carrying the event data.
        event_id: Optional UUID for idempotent tracking.
        extra_attributes: Optional string-only key/value pairs attached as Pub/Sub attributes.
        topic_id_override: Optional topic ID to publish to instead of the default.

    Returns:
        PublishResponse containing the Pub/Sub message ID and event ID.
    """
    request = PublishRequest(
        event_type=event_type,
        source=source,
        payload=payload,
        event_id=event_id,
    )

    publisher: pubsub_v1.PublisherClient = get_publisher()
    target_topic = topic_path(topic_id_override)

    data_bytes = normalize_payload(request.payload)

    attrs = build_attributes(
        event_id=request.event_id,
        event_type=request.event_type,
        source=request.source,
        extra=extra_attributes,
    )

    future = publisher.publish(target_topic, data_bytes, **attrs)
    message_id = future.result()

    return PublishResponse(
        message_id=message_id,
        event_id=request.event_id,
        acknowledged=True,
    )


if __name__ == "__main__":
    resp = publish_event(
        event_type="user.signup",
        source="auth-service",
        payload={"username": "alice", "email": "alice@example.com"},
    )
    print(json.dumps({"message_id": resp.message_id, "event_id": resp.event_id}))
