import json
import os
from messaging_models import PubSubEvent, PublishResult, validate_event
from messaging_client import topic_path, publish_message, validate_config


def publish_event(event: PubSubEvent) -> PublishResult:
    errors = validate_event(event)
    if errors:
        return PublishResult(
            message_id="",
            success=False,
            error="; ".join(errors),
        )

    config_errors = validate_config()
    if config_errors:
        return PublishResult(
            message_id="",
            success=False,
            error="; ".join(config_errors),
        )

    topic = topic_path()
    data = event.to_json().encode("utf-8")
    attributes = {
        "event_type": event.event_type,
        "source": event.source,
        "event_id": event.event_id,
    }
    if event.correlation_id:
        attributes["correlation_id"] = event.correlation_id

    try:
        message_id = publish_message(topic, data, attributes)
        return PublishResult(
            message_id=message_id,
            success=True,
            topic=topic,
        )
    except Exception as exc:
        return PublishResult(
            message_id="",
            success=False,
            error=str(exc),
        )


def main():
    raw = os.environ.get(
        "EVENT_PAYLOAD",
        '{"event_type":"order.created","source":"api","payload":{"order_id":"12345"}}',
    )
    event_data = json.loads(raw)
    event = PubSubEvent.from_dict(event_data)
    result = publish_event(event)
    print(json.dumps(result.to_dict()))


if __name__ == "__main__":
    main()
