import os
from google.cloud import pubsub_v1

from messaging_client import (
    get_project_id,
    get_pubsub_publisher_client,
    topic_path,
    load_topic_config,
)
from messaging_models import EventMessage, PublishResult, normalize_payload


def publish_event(
    event_type: str,
    source: str,
    payload: dict,
    attributes: dict | None = None,
    topic_name: str | None = None,
    project_id: str | None = None,
) -> PublishResult:
    project_id = project_id or get_project_id()
    config = load_topic_config()
    topic_name = topic_name or config["topic_name"]

    normalized = normalize_payload(payload)
    event = EventMessage.create(
        event_type=event_type,
        source=source,
        payload=normalized,
        attributes=attributes,
    )

    publisher = get_pubsub_publisher_client()
    topic = topic_path(project_id, topic_name)

    publish_attrs = {
        "event_type": event.event_type,
        "event_id": event.event_id,
        "source": event.source,
    }
    if attributes:
        publish_attrs.update({k: str(v) for k, v in attributes.items()})

    future = publisher.publish(
        topic,
        data=event.to_pubsub_data(),
        **publish_attrs,
    )
    message_id = future.result()

    return PublishResult(
        message_id=message_id,
        event_id=event.event_id,
        status="published",
        timestamp=event.timestamp,
    )


if __name__ == "__main__":
    result = publish_event(
        event_type="order.created",
        source="order-service",
        payload={"order_id": "ORD-12345", "total": 99.99},
        attributes={"priority": "high"},
    )
    print(result.to_dict())
