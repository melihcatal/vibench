"""Publishes a batch of messages with IDs or attributes to Google Cloud Pub/Sub.

Uses the google.cloud.pubsub_v1 PublisherClient to publish multiple events
in a batch operation, with per-message attributes and batch-level configuration.
"""

import uuid
from datetime import datetime, timezone

from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.types import PublishBatchSettings

from messaging_client import get_publisher_client, topic_path
from messaging_models import PubSubEvent, PublishResult, build_message_attributes


def batch_publish_events(
    events: list[PubSubEvent],
    project_id: str | None = None,
    topic_id: str | None = None,
    client: PublisherClient | None = None,
    batch_size: int = 10,
    max_latency: float = 1.0,
) -> PublishResult:
    """Publish a batch of events to a Google Cloud Pub/Sub topic.

    Publishes multiple PubSubEvent objects to the specified topic using
    the PublisherClient's batch publish capabilities. Each event is published
    with its own attributes derived from the event metadata.

    Args:
        events: List of PubSubEvent objects to publish.
        project_id: GCP project ID. Uses default if not provided.
        topic_id: Pub/Sub topic ID. Uses default if not provided.
        client: Optional pre-configured PublisherClient.
        batch_size: Maximum messages per batch. Defaults to 10.
        max_latency: Maximum seconds before flushing a batch. Defaults to 1.0.

    Returns:
        PublishResult containing all message IDs and the topic path.

    Raises:
        Exception: If any publish operation fails.
    """
    publisher = client or get_publisher_client(
        batch_size=batch_size, max_latency=max_latency
    )
    topic = topic_path(project_id, topic_id)

    futures = []
    for event in events:
        data = event.to_json_bytes()
        attributes = build_message_attributes(
            event_type=event.event_type,
            source=event.source,
            extra={
                "event_id": event.event_id,
                "created_at": event.created_at,
            },
        )
        future = publisher.publish(topic, data, **attributes)
        futures.append((event.event_id, future))

    message_ids = []
    for event_id, future in futures:
        message_id = future.result()
        message_ids.append(message_id)

    return PublishResult(
        message_ids=message_ids,
        topic=topic,
        count=len(message_ids),
    )


def batch_publish_raw(
    messages: list[dict],
    event_type: str = "batch.event",
    source: str = "batch-publisher",
    project_id: str | None = None,
    topic_id: str | None = None,
    client: PublisherClient | None = None,
    batch_size: int = 10,
    max_latency: float = 1.0,
) -> PublishResult:
    """Publish a batch of raw message dictionaries to a Google Cloud Pub/Sub topic.

    Converts raw dictionaries into PubSubEvent objects with auto-generated IDs
    and publishes them as a batch.

    Args:
        messages: List of dictionaries to publish as event payloads.
        event_type: Event type for all messages in the batch.
        source: Source identifier for all messages.
        project_id: GCP project ID.
        topic_id: Pub/Sub topic ID.
        client: Optional pre-configured PublisherClient.
        batch_size: Maximum messages per batch.
        max_latency: Maximum seconds before flushing a batch.

    Returns:
        PublishResult with all published message IDs.
    """
    events = []
    batch_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc).isoformat()

    for idx, payload in enumerate(messages):
        event = PubSubEvent(
            event_type=event_type,
            payload=payload,
            source=source,
            attributes={
                "batch_id": batch_id,
                "batch_index": str(idx),
            },
        )
        events.append(event)

    return batch_publish_events(
        events,
        project_id=project_id,
        topic_id=topic_id,
        client=client,
        batch_size=batch_size,
        max_latency=max_latency,
    )


def batch_publish_with_custom_attributes(
    payloads: list[tuple[dict, dict[str, str]]],
    project_id: str | None = None,
    topic_id: str | None = None,
    client: PublisherClient | None = None,
    batch_size: int = 10,
    max_latency: float = 1.0,
) -> PublishResult:
    """Publish a batch of messages each with custom attributes.

    Args:
        payloads: List of tuples (payload_dict, attributes_dict).
        project_id: GCP project ID.
        topic_id: Pub/Sub topic ID.
        client: Optional pre-configured PublisherClient.
        batch_size: Maximum messages per batch.
        max_latency: Maximum seconds before flushing a batch.

    Returns:
        PublishResult with all published message IDs.
    """
    events = []
    for payload, attrs in payloads:
        event_type = attrs.get("event_type", "custom.event")
        source = attrs.get("source", "custom-source")
        event = PubSubEvent(
            event_type=event_type,
            payload=payload,
            source=source,
            attributes=attrs,
        )
        events.append(event)

    return batch_publish_events(
        events,
        project_id=project_id,
        topic_id=topic_id,
        client=client,
        batch_size=batch_size,
        max_latency=max_latency,
    )


if __name__ == "__main__":
    messages = [
        {"user_id": "U001", "action": "login"},
        {"user_id": "U002", "action": "purchase", "amount": 49.99},
        {"user_id": "U003", "action": "logout"},
    ]
    result = batch_publish_raw(
        messages,
        event_type="user.activity",
        source="user-service",
    )
    print(f"Published {result.count} messages to {result.topic}")
    print(f"Message IDs: {result.message_ids}")
