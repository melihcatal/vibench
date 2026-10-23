"""
Publish a batch of messages with IDs or attributes to a Google Cloud Pub/Sub topic.

Uses the google-cloud-pubsub SDK to publish multiple messages in a single
batch operation, authenticated via GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
import uuid
import time
from typing import Any
from messaging_client import (
    get_publisher_client,
    topic_path,
    ensure_topic_exists,
    publish_batch_sync,
)
from messaging_models import PubSubEvent, PublishResult, normalize_payload, build_attributes


def batch_publish(
    events: list[dict[str, Any]],
    topic_name: str | None = None,
) -> list[PublishResult]:
    """
    Publish a batch of events to a Google Cloud Pub/Sub topic.

    Each event dict should contain:
        - event_type (str): The type/category of the event.
        - payload (dict): The event payload dictionary.
        - source (str, optional): Source identifier.
        - attributes (dict, optional): Pub/Sub message attributes.

    Args:
        events: List of event dictionaries to publish.
        topic_name: Override the default topic name.

    Returns:
        List of PublishResult objects, one per published message.
    """
    publisher = get_publisher_client()
    topic = ensure_topic_exists(topic_name=topic_name)

    messages: list[dict] = []
    events_info: list[tuple[str, str]] = []

    for idx, event_data in enumerate(events):
        event_type = event_data.get("event_type", "batch_event")
        payload = normalize_payload(event_data.get("payload", {}))
        source = event_data.get("source", "batch_publish")
        attrs = event_data.get("attributes", {})

        event = PubSubEvent(
            event_id=event_data.get("event_id", str(uuid.uuid4())),
            event_type=event_type,
            payload=payload,
            timestamp=time.time(),
            source=source,
            attributes=build_attributes(attrs) if attrs else {},
        )

        messages.append({
            "data": event.to_bytes(),
            "attributes": event.attributes if event.attributes else None,
        })
        events_info.append((event.event_id, event.event_type))

    message_ids = publish_batch_sync(publisher=publisher, topic=topic, messages=messages)

    results: list[PublishResult] = []
    for mid, (eid, _) in zip(message_ids, events_info):
        results.append(
            PublishResult(
                message_id=mid,
                event_id=eid,
                topic=topic,
                success=True,
            )
        )

    return results


if __name__ == "__main__":
    batch_events = [
        {
            "event_type": "user.login",
            "payload": {"user_id": "u001", "ip": "10.0.0.1"},
            "source": "auth_service",
            "attributes": {"priority": "low"},
        },
        {
            "event_type": "order.created",
            "payload": {"order_id": "o001", "total": 59.99},
            "source": "order_service",
            "attributes": {"priority": "high"},
        },
        {
            "event_type": "notification.sent",
            "payload": {"channel": "email", "recipient": "user@example.com"},
            "source": "notification_service",
            "attributes": {"priority": "medium"},
        },
    ]
    results = batch_publish(events=batch_events)
    print(json.dumps([r.to_dict() for r in results], indent=2))
