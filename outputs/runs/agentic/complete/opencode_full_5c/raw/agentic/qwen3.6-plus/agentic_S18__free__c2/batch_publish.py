from google.cloud.pubsub_v1 import PublisherClient

from messaging_client import (
    create_publisher_client,
    get_topic_path,
    ensure_topic_exists,
)
from messaging_models import PubSubEvent, BatchPublishResult


def batch_publish(events: list[PubSubEvent]) -> BatchPublishResult:
    publisher: PublisherClient = create_publisher_client()
    topic_path = get_topic_path()
    ensure_topic_exists(publisher, topic_path)

    message_ids = []
    event_ids = []

    for event in events:
        payload_bytes = event.to_json().encode("utf-8")

        attributes = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "timestamp": event.timestamp,
            "batch_member": "true",
        }
        attributes.update(event.attributes)

        future = publisher.publish(
            topic=topic_path,
            data=payload_bytes,
            **attributes,
        )
        message_id = future.result()
        message_ids.append(message_id)
        event_ids.append(event.event_id)

    return BatchPublishResult(
        message_ids=message_ids,
        event_ids=event_ids,
        total_published=len(message_ids),
        status="batch_published",
    )


if __name__ == "__main__":
    import json
    import sys

    raw = (
        sys.stdin.read()
        if not sys.stdin.isatty()
        else '[{"event_type":"order","source":"api","payload":{"order_id":"1"}},{"event_type":"order","source":"api","payload":{"order_id":"2"}}]'
    )
    events_data = json.loads(raw)
    events = [PubSubEvent.from_dict(e) for e in events_data]
    result = batch_publish(events)
    print(json.dumps(result.to_dict(), indent=2))
