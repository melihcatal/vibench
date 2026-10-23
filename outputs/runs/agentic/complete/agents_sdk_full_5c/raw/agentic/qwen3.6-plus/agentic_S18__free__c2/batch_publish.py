"""Publish a batch of messages with IDs or attributes via Google Cloud Pub/Sub."""

import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import BatchSettings

from messaging_client import get_pubsub_publisher_client, get_pubsub_config
from messaging_models import EventMessage, BatchPublishResponse, PublishResponse


def batch_publish_events(
    events: List[EventMessage],
    topic_id: str,
    batch_size: int = 10,
    batch_max_latency: float = 5.0,
) -> BatchPublishResponse:
    """Publish a batch of events to a Google Cloud Pub/Sub topic.

    Args:
        events: List of EventMessage objects to publish.
        topic_id: Google Cloud Pub/Sub topic name.
        batch_size: Number of messages per batch.
        batch_max_latency: Maximum seconds to wait before flushing batch.

    Returns:
        BatchPublishResponse with results for all published messages.
    """
    config = get_pubsub_config()
    project_id = config["project_id"]

    batch_settings = BatchSettings(
        max_messages=batch_size,
        max_latency=batch_max_latency,
    )

    publisher_client = pubsub_v1.PublisherClient(
        batch_settings=batch_settings
    )
    topic_path = publisher_client.topic_path(project_id, topic_id)

    results: List[PublishResponse] = []
    errors: List[Dict[str, Any]] = []

    for event in events:
        payload = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "payload": event.payload,
            "metadata": event.metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "batch_id": event.metadata.get("batch_id", str(uuid.uuid4())),
        }

        message_body = json.dumps(payload).encode("utf-8")

        attributes = {
            "event_type": event.event_type,
            "source": event.source,
            "event_id": event.event_id,
            "content_type": "application/json",
        }

        try:
            future = publisher_client.publish(
                topic_path, data=message_body, **attributes
            )
            message_id = future.result()

            results.append(
                PublishResponse(
                    message_id=message_id,
                    event_id=event.event_id,
                    topic_path=topic_path,
                    status="published",
                )
            )
        except Exception as e:
            errors.append(
                {
                    "event_id": event.event_id,
                    "error": str(e),
                    "status": "failed",
                }
            )

    publisher_client.stop()

    return BatchPublishResponse(
        topic_path=topic_path,
        published_count=len(results),
        failed_count=len(errors),
        results=results,
        errors=errors,
    )


def batch_publish_dicts(
    event_dicts: List[Dict[str, Any]],
    topic_id: str,
    batch_size: int = 10,
) -> BatchPublishResponse:
    """Publish a batch of event dictionaries to Google Cloud Pub/Sub.

    Args:
        event_dicts: List of dictionaries representing events.
        topic_id: Google Cloud Pub/Sub topic name.
        batch_size: Number of messages per batch.

    Returns:
        BatchPublishResponse with results for all published messages.
    """
    events = [
        EventMessage(
            event_id=ed.get("event_id", str(uuid.uuid4())),
            event_type=ed.get("event_type", "custom"),
            source=ed.get("source", "api"),
            payload=ed.get("payload", {}),
            metadata=ed.get("metadata", {}),
        )
        for ed in event_dicts
    ]
    return batch_publish_events(events, topic_id, batch_size=batch_size)
