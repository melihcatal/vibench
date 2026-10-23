from google.cloud import pubsub_v1
from messaging_client import (
    get_publisher_client,
    topic_path,
    load_topic_config,
    build_publish_request,
)
from messaging_models import (
    PubSubEvent,
    PublishResult,
    normalize_payload,
    normalize_attributes,
    build_event_dict,
)


def publish_event(event: PubSubEvent, topic_name: str | None = None) -> PublishResult:
    config = load_topic_config()
    project_id = config["project_id"]
    topic = topic_name or config["topic_name"]
    tp = topic_path(project_id, topic)
    publisher = get_publisher_client()

    event_dict = build_event_dict(event)
    event_data = event.to_json().encode("utf-8")

    attrs = normalize_attributes(event.attributes)
    attrs["event_type"] = event.event_type
    attrs["source"] = event.source
    attrs["event_id"] = event.event_id

    request = build_publish_request(event_data, attrs)
    future = publisher.publish(tp, **request)
    message_id = future.result()

    return PublishResult(
        message_id=message_id,
        event_id=event.event_id,
        topic=tp,
        acknowledged=True,
    )


if __name__ == "__main__":
    evt = PubSubEvent(
        event_type="order.created",
        source="order-service",
        payload=normalize_payload({"order_id": "ORD-12345", "amount": 99.99}),
        attributes={"priority": "high"},
    )
    result = publish_event(evt)
    print(result.to_dict())
