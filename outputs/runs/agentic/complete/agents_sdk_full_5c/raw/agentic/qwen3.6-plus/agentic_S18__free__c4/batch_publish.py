"""Publish a batch of messages with IDs and attributes to Google Cloud Pub/Sub.

Uses the google-cloud-pubsub SDK to publish multiple messages efficiently
to a managed topic with per-message attributes and ordering keys.
"""

import os
import json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from google.cloud import pubsub_v1


def batch_publish(
    messages: List[Dict[str, Any]],
    topic_path: Optional[str] = None,
    ordering_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Publish a batch of messages to a Google Cloud Pub/Sub topic.

    Args:
        messages: List of message dicts. Each should have 'payload' key and
            optionally 'attributes', 'event_type', and 'message_id'.
        topic_path: Full topic path. Auto-constructed from env if not provided.
        ordering_key: Optional ordering key for message ordering.

    Returns:
        Dict with batch publish results including all message IDs.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pubsub-project-001")
    topic_name = os.environ.get("PUBSUB_TOPIC", "events-topic")

    if topic_path is None:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)

    publisher = pubsub_v1.PublisherClient()

    publish_futures = []
    message_metadata = []

    for idx, msg in enumerate(messages):
        payload = msg.get("payload", {})
        event_type = msg.get("event_type", "batch.item")
        message_id = msg.get("message_id", str(uuid.uuid4()))
        msg_attributes = msg.get("attributes", {})

        event_data = {
            "event_id": message_id,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "batch_index": idx,
            "payload": payload,
        }

        message_body = json.dumps(event_data).encode("utf-8")

        attrs = {
            "event_type": event_type,
            "event_id": message_id,
            "batch_index": str(idx),
            "content_type": "application/json",
        }
        attrs.update(msg_attributes)

        publish_kwargs = {"data": message_body, **attrs}
        if ordering_key:
            publish_kwargs["ordering_key"] = f"{ordering_key}-{idx}"

        future = publisher.publish(topic_path, **publish_kwargs)
        publish_futures.append((message_id, event_type, future))

    for message_id, event_type, future in publish_futures:
        published_id = future.result()
        message_metadata.append({
            "event_id": message_id,
            "event_type": event_type,
            "pubsub_message_id": published_id,
            "status": "published",
        })

    return {
        "status": "batch_published",
        "topic": topic_path,
        "count": len(message_metadata),
        "messages": message_metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def publish_ordered_batch(
    messages: List[Dict[str, Any]],
    topic_path: Optional[str] = None,
    ordering_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Publish an ordered batch of messages using Pub/Sub message ordering.

    Messages with the same ordering key are delivered in publish order.

    Args:
        messages: List of message dicts with 'payload' and optional metadata.
        topic_path: Full topic path.
        ordering_key: Required ordering key for guaranteed order delivery.

    Returns:
        Dict with ordered batch publish results.
    """
    if not ordering_key:
        raise ValueError("ordering_key is required for ordered batch publishing")

    batch_id = f"ordered-{uuid.uuid4().hex[:8]}"

    ordered_messages = []
    for idx, msg in enumerate(messages):
        msg_with_meta = dict(msg)
        msg_with_meta.setdefault("message_id", f"{batch_id}-{idx}")
        msg_with_meta.setdefault("event_type", "ordered.item")
        msg_with_meta.setdefault("attributes", {})
        msg_with_meta["attributes"]["ordering_key"] = ordering_key
        msg_with_meta["attributes"]["batch_id"] = batch_id
        ordered_messages.append(msg_with_meta)

    result = batch_publish(ordered_messages, topic_path=topic_path, ordering_key=ordering_key)
    result["batch_id"] = batch_id
    result["ordering_key"] = ordering_key

    return result


if __name__ == "__main__":
    sample_messages = [
        {"payload": {"item": "A", "value": 1}, "event_type": "item.processed"},
        {"payload": {"item": "B", "value": 2}, "event_type": "item.processed"},
        {"payload": {"item": "C", "value": 3}, "event_type": "item.processed"},
    ]

    result = batch_publish(sample_messages)
    print(json.dumps(result, indent=2))
