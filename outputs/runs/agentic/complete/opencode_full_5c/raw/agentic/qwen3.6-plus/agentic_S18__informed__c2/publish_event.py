import json
from messaging_client import (
    load_config,
    get_publisher_client,
    build_topic_path,
    publish_raw_message,
)
from messaging_models import EventMessage, PublishResult, sanitize_event_attributes


def publish_event(
    event_data: dict, event_type: str = "", source: str = ""
) -> PublishResult:
    config = load_config()
    publisher = get_publisher_client()
    topic_path = build_topic_path(config)

    event = EventMessage(
        event_type=event_type or event_data.get("event_type", "generic"),
        source=source or event_data.get("source", "unknown"),
        payload=event_data.get("payload", event_data),
        attributes=event_data.get("attributes", {}),
    )

    payload_bytes = event.to_json().encode("utf-8")
    attributes = sanitize_event_attributes(
        {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            **event.attributes,
        }
    )

    message_id = publish_raw_message(publisher, topic_path, payload_bytes, attributes)

    return PublishResult(
        message_id=message_id,
        event_id=event.event_id,
        status="published",
        timestamp=event.timestamp,
    )


if __name__ == "__main__":
    result = publish_event(
        {
            "event_type": "order.created",
            "source": "checkout-service",
            "payload": {"order_id": "ORD-12345", "amount": 99.99, "currency": "USD"},
            "attributes": {"priority": "high", "region": "us-east-1"},
        }
    )
    print(json.dumps(result.to_dict(), indent=2))
