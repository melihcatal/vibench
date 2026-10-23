import os
import uuid
from datetime import datetime, timezone

from google.cloud import pubsub_v1

from messaging_client import (
    get_project_id,
    get_pubsub_publisher_client,
    topic_path,
    load_topic_config,
)
from messaging_models import (
    EventMessage,
    PublishResult,
    BatchPublishResult,
    normalize_payload,
)


def batch_publish(
    events: list[dict],
    topic_name: str | None = None,
    project_id: str | None = None,
) -> BatchPublishResult:
    project_id = project_id or get_project_id()
    config = load_topic_config()
    topic_name = topic_name or config["topic_name"]

    publisher = get_pubsub_publisher_client()
    topic = topic_path(project_id, topic_name)

    batch_id = str(uuid.uuid4())
    results = []
    success_count = 0
    failure_count = 0

    for item in events:
        payload = normalize_payload(item.get("payload", {}))
        attributes = item.get("attributes", {})
        event = EventMessage.create(
            event_type=item["event_type"],
            source=item["source"],
            payload=payload,
            attributes=attributes,
        )

        publish_attrs = {
            "event_type": event.event_type,
            "event_id": event.event_id,
            "source": event.source,
            "batch_id": batch_id,
        }
        if attributes:
            publish_attrs.update({k: str(v) for k, v in attributes.items()})

        try:
            future = publisher.publish(
                topic,
                data=event.to_pubsub_data(),
                **publish_attrs,
            )
            message_id = future.result()
            results.append(
                PublishResult(
                    message_id=message_id,
                    event_id=event.event_id,
                    status="published",
                    timestamp=event.timestamp,
                )
            )
            success_count += 1
        except Exception as exc:
            results.append(
                PublishResult(
                    message_id="",
                    event_id=event.event_id,
                    status=f"failed: {exc}",
                    timestamp=event.timestamp,
                )
            )
            failure_count += 1

    return BatchPublishResult(
        batch_id=batch_id,
        results=results,
        success_count=success_count,
        failure_count=failure_count,
    )


if __name__ == "__main__":
    events = [
        {
            "event_type": "user.signup",
            "source": "auth-service",
            "payload": {"user_id": "U1"},
        },
        {
            "event_type": "user.signup",
            "source": "auth-service",
            "payload": {"user_id": "U2"},
        },
        {
            "event_type": "order.placed",
            "source": "order-service",
            "payload": {"order_id": "O1"},
        },
    ]
    result = batch_publish(events)
    print(result.to_dict())
