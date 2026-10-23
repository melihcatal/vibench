"""Publishes a JSON event to a Google Cloud Pub/Sub managed messaging topic.

Uses the google.cloud.pubsub_v1 PublisherClient to publish structured events
to a managed Pub/Sub topic with configurable attributes and payload.
"""

import json
from google.cloud.pubsub_v1 import PublisherClient

from messaging_client import get_publisher_client, topic_path
from messaging_models import PubSubEvent, PublishResult, build_message_attributes


def publish_event(
    event: PubSubEvent,
    project_id: str | None = None,
    topic_id: str | None = None,
    client: PublisherClient | None = None,
) -> PublishResult:
    """Publish a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event: The PubSubEvent to publish.
        project_id: GCP project ID. Uses default if not provided.
        topic_id: Pub/Sub topic ID. Uses default if not provided.
        client: Optional pre-configured PublisherClient. Creates one if None.

    Returns:
        PublishResult containing the message ID and topic path.

    Raises:
        Exception: If the publish operation fails.
    """
    publisher = client or get_publisher_client()
    topic = topic_path(project_id, topic_id)

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
    message_id = future.result()

    return PublishResult(
        message_ids=[message_id],
        topic=topic,
        count=1,
    )


def publish_raw_event(
    event_type: str,
    payload: dict,
    source: str = "default",
    project_id: str | None = None,
    topic_id: str | None = None,
    extra_attributes: dict[str, str] | None = None,
    client: PublisherClient | None = None,
) -> PublishResult:
    """Publish a raw event dictionary to a Google Cloud Pub/Sub topic.

    Convenience wrapper that constructs a PubSubEvent and publishes it.

    Args:
        event_type: Classification string for the event.
        payload: JSON-serializable dictionary payload.
        source: Origin identifier for the event.
        project_id: GCP project ID.
        topic_id: Pub/Sub topic ID.
        extra_attributes: Optional additional Pub/Sub message attributes.
        client: Optional pre-configured PublisherClient.

    Returns:
        PublishResult with the published message ID.
    """
    event = PubSubEvent(
        event_type=event_type,
        payload=payload,
        source=source,
        attributes=extra_attributes or {},
    )
    return publish_event(event, project_id=project_id, topic_id=topic_id, client=client)


if __name__ == "__main__":
    result = publish_raw_event(
        event_type="order.created",
        payload={"order_id": "ORD-12345", "amount": 99.99},
        source="order-service",
    )
    print(f"Published event to {result.topic}: {result.message_ids}")
