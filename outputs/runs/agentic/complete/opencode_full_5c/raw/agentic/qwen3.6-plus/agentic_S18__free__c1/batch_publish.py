import uuid
from typing import Optional, List

from messaging_client import get_publisher_client, topic_path
from messaging_models import (
    BatchPublishResult,
    EventMessage,
    normalize_payload,
    build_event_attributes,
)


def batch_publish(
    events: List[dict],
    event_type: str = "batch.event",
    source: str = "batch_publisher",
    topic_id: Optional[str] = None,
) -> BatchPublishResult:
    publisher = get_publisher_client()
    topic = topic_path(topic_id)

    result = BatchPublishResult(topic_path=topic)
    futures = []

    for idx, event_data in enumerate(events):
        payload = normalize_payload(event_data)
        event = EventMessage(
            event_type=event_type,
            source=source,
            payload=payload,
            attributes={"batch_index": str(idx)},
        )

        data_bytes = event.to_json().encode("utf-8")
        attributes = build_event_attributes(event)

        try:
            future = publisher.publish(topic, data=data_bytes, **attributes)
            futures.append((future, event))
        except Exception as exc:
            result.total_failed += 1
            result.errors.append(
                {
                    "index": idx,
                    "error": str(exc),
                }
            )

    for future, event in futures:
        try:
            message_id = future.result(timeout=30.0)
            result.message_ids.append(message_id)
            result.event_ids.append(event.event_id)
            result.total_published += 1
        except Exception as exc:
            result.total_failed += 1
            result.errors.append(
                {
                    "event_id": event.event_id,
                    "error": str(exc),
                }
            )

    return result


def batch_publish_with_ids(
    messages: List[dict],
    topic_id: Optional[str] = None,
) -> BatchPublishResult:
    publisher = get_publisher_client()
    topic = topic_path(topic_id)

    result = BatchPublishResult(topic_path=topic)
    futures = []

    for msg in messages:
        event_id = msg.get("event_id", str(uuid.uuid4()))
        event_type = msg.get("event_type", "custom.event")
        source = msg.get("source", "batch_publisher")
        payload = normalize_payload(msg.get("payload", {}))
        attributes = msg.get("attributes", {})

        event = EventMessage(
            event_id=event_id,
            event_type=event_type,
            source=source,
            payload=payload,
            attributes=attributes,
        )

        data_bytes = event.to_json().encode("utf-8")
        pub_attributes = build_event_attributes(event)

        try:
            future = publisher.publish(topic, data=data_bytes, **pub_attributes)
            futures.append((future, event))
        except Exception as exc:
            result.total_failed += 1
            result.errors.append(
                {
                    "event_id": event_id,
                    "error": str(exc),
                }
            )

    for future, event in futures:
        try:
            message_id = future.result(timeout=30.0)
            result.message_ids.append(message_id)
            result.event_ids.append(event.event_id)
            result.total_published += 1
        except Exception as exc:
            result.total_failed += 1
            result.errors.append(
                {
                    "event_id": event.event_id,
                    "error": str(exc),
                }
            )

    return result
