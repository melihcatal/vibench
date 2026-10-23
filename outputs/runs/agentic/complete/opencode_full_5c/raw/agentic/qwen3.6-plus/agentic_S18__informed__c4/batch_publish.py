from google.cloud import pubsub_v1
from messaging_client import (
    get_publisher_client,
    topic_path,
    load_topic_config,
    build_publish_request,
)
from messaging_models import (
    PubSubEvent,
    BatchPublishResult,
    normalize_attributes,
    build_event_dict,
)


def batch_publish(
    events: list[PubSubEvent], topic_name: str | None = None
) -> BatchPublishResult:
    config = load_topic_config()
    project_id = config["project_id"]
    topic = topic_name or config["topic_name"]
    tp = topic_path(project_id, topic)
    publisher = get_publisher_client()

    successful_ids = []
    failed_ids = []

    for event in events:
        event_data = event.to_json().encode("utf-8")
        attrs = normalize_attributes(event.attributes)
        attrs["event_type"] = event.event_type
        attrs["source"] = event.source
        attrs["event_id"] = event.event_id

        request = build_publish_request(event_data, attrs)
        try:
            future = publisher.publish(tp, **request)
            message_id = future.result()
            successful_ids.append(message_id)
        except Exception:
            failed_ids.append(event.event_id)

    return BatchPublishResult(
        total_messages=len(events),
        successful_ids=successful_ids,
        failed_ids=failed_ids,
        topic=tp,
    )


if __name__ == "__main__":
    events = [
        PubSubEvent(
            event_type="order.created",
            source="order-service",
            payload={"order_id": "ORD-1"},
        ),
        PubSubEvent(
            event_type="order.created",
            source="order-service",
            payload={"order_id": "ORD-2"},
        ),
        PubSubEvent(
            event_type="order.created",
            source="order-service",
            payload={"order_id": "ORD-3"},
        ),
    ]
    result = batch_publish(events)
    print(result.to_dict())
