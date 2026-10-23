from google.cloud.pubsub_v1 import PublisherClient

from messaging_client import (
    create_publisher_client,
    get_topic_path,
    ensure_topic_exists,
)
from messaging_models import PubSubEvent, PublishResult


def publish_event(event: PubSubEvent) -> PublishResult:
    publisher: PublisherClient = create_publisher_client()
    topic_path = get_topic_path()
    ensure_topic_exists(publisher, topic_path)

    payload_bytes = event.to_json().encode("utf-8")

    attributes = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "source": event.source,
        "timestamp": event.timestamp,
    }
    attributes.update(event.attributes)

    future = publisher.publish(
        topic=topic_path,
        data=payload_bytes,
        **attributes,
    )
    message_id = future.result()

    return PublishResult(
        message_id=message_id,
        event_id=event.event_id,
        status="published",
    )


if __name__ == "__main__":
    import json
    import sys

    raw = (
        sys.stdin.read()
        if not sys.stdin.isatty()
        else '{"event_type":"test","source":"cli","payload":{"msg":"hello"}}'
    )
    event_data = json.loads(raw)
    event = PubSubEvent.from_dict(event_data)
    result = publish_event(event)
    print(json.dumps(result.to_dict()))
