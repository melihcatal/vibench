"""
[SAME-SCENARIO] Publish a batch of messages with IDs or attributes to Google Cloud Pub/Sub.
Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from messaging_models import PubSubEvent, BatchPublishResult
from messaging_client import get_pubsub_publisher_client, get_topic_path


def batch_publish(
    events: List[PubSubEvent],
    topic_id: str = None,
    project_id: str = None,
) -> BatchPublishResult:
    """
    Publish a batch of events to a Google Cloud Pub/Sub topic.

    Each event is published with its own event_id, type, and source
    as Pub/Sub message attributes.

    Args:
        events: List of PubSubEvent objects to publish.
        topic_id: The Pub/Sub topic identifier.
        project_id: The GCP project ID.

    Returns:
        BatchPublishResult with published/failed counts and message IDs.
    """
    topic_id = topic_id or os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
    publisher = get_pubsub_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    result = BatchPublishResult()

    for event in events:
        try:
            message_bytes = event.to_json().encode("utf-8")
            attributes = {
                "event_type": event.event_type,
                "source": event.source,
                "event_id": event.event_id,
            }
            attributes.update(event.attributes)

            future = publisher.publish(topic_path, data=message_bytes, **attributes)
            message_id = future.result(timeout=30)

            result.published_count += 1
            result.message_ids.append(message_id)

        except Exception as exc:
            result.failed_count += 1
            result.errors.append({
                "event_id": event.event_id,
                "error": str(exc),
            })

    return result


def batch_publish_dicts(
    messages: List[Dict[str, Any]],
    topic_id: str = None,
    project_id: str = None,
) -> BatchPublishResult:
    """
    Publish a batch of messages provided as dictionaries.

    Each dict should have: event_type, payload. Optional: event_id, source, attributes.

    Args:
        messages: List of message dictionaries.
        topic_id: The Pub/Sub topic identifier.
        project_id: The GCP project ID.

    Returns:
        BatchPublishResult with counts, message IDs, and any errors.
    """
    events = []
    for msg in messages:
        event = PubSubEvent(
            event_id=msg.get("event_id", str(uuid.uuid4())),
            event_type=msg.get("event_type", "unknown"),
            source=msg.get("source", "batch"),
            payload=msg.get("payload", msg),
            attributes=msg.get("attributes", {}),
        )
        events.append(event)

    return batch_publish(events, topic_id, project_id)
