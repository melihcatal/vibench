"""Publish a JSON event to a Google Cloud Pub/Sub topic.

Uses the google-cloud-pubsub SDK to publish events to a managed messaging topic.
Requires the topic to exist in the configured GCP project.
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from google.cloud import pubsub_v1


def publish_event(
    topic_path: Optional[str] = None,
    event_type: str = "order.created",
    payload: Optional[Dict[str, Any]] = None,
    event_id: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Publish a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_path: Full topic path like "projects/<project-id>/topics/<topic-name>".
        event_type: Type identifier for the event.
        payload: Dictionary payload to be serialized as JSON.
        event_id: Unique event identifier. Auto-generated if not provided.
        attributes: Additional Pub/Sub message attributes.

    Returns:
        Dict with publish result including message ID and topic.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pubsub-project-001")
    topic_name = os.environ.get("PUBSUB_TOPIC", "events-topic")

    if topic_path is None:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)

    if payload is None:
        payload = {"data": "sample_event"}

    if event_id is None:
        import uuid
        event_id = str(uuid.uuid4())

    event_data = {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }

    message_body = json.dumps(event_data).encode("utf-8")

    msg_attributes = {
        "event_type": event_type,
        "event_id": event_id,
        "content_type": "application/json",
    }
    if attributes:
        msg_attributes.update(attributes)

    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(topic_path, message_body, **msg_attributes)
    message_id = future.result()

    return {
        "status": "published",
        "topic": topic_path,
        "message_id": message_id,
        "event_id": event_id,
        "event_type": event_type,
    }


if __name__ == "__main__":
    result = publish_event(
        event_type="order.created",
        payload={"order_id": "ORD-12345", "amount": 99.99, "currency": "USD"},
    )
    print(json.dumps(result, indent=2))
