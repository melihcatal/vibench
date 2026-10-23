"""
Publish a JSON event to a Google Cloud Pub/Sub managed messaging topic.

Uses the google-cloud-pubsub SDK to connect to the Pub/Sub service
authenticated via GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
import sys
from messaging_client import (
    get_publisher_client,
    topic_path,
    ensure_topic_exists,
    publish_message_sync,
)
from messaging_models import PubSubEvent, PublishResult, normalize_payload, build_attributes


def publish_event(
    event_type: str,
    payload: dict,
    source: str = "publish_event",
    attributes: dict[str, str] | None = None,
    topic_name: str | None = None,
) -> PublishResult:
    """
    Publish a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event_type: The type/category of the event being published.
        payload: The event payload dictionary (will be normalized).
        source: Optional source identifier.
        attributes: Optional Pub/Sub message attributes (key/value string pairs).
        topic_name: Override the default topic name.

    Returns:
        PublishResult containing the message ID and status.
    """
    normalized = normalize_payload(payload)
    event = PubSubEvent(
        event_type=event_type,
        payload=normalized,
        source=source,
        attributes=build_attributes(attributes) if attributes else {},
    )

    publisher = get_publisher_client()
    topic = ensure_topic_exists(topic_name=topic_name)

    attributes_dict = event.attributes if event.attributes else None
    message_id = publish_message_sync(
        publisher=publisher,
        topic=topic,
        data=event.to_bytes(),
        attributes=attributes_dict,
    )

    return PublishResult(
        message_id=message_id,
        event_id=event.event_id,
        topic=topic,
        success=True,
    )


if __name__ == "__main__":
    sample_payload = {
        "user_id": "usr_12345",
        "action": "signup_completed",
        "metadata": {"channel": "web", "referrer": "organic"},
    }
    result = publish_event(
        event_type="user.signup",
        payload=sample_payload,
        source="publish_event_cli",
        attributes={"priority": "high", "region": "us-east1"},
    )
    print(json.dumps(result.to_dict(), indent=2))
