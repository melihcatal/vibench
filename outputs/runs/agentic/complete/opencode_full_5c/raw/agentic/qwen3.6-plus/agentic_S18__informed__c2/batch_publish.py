import json
import uuid
from messaging_client import (
    load_config,
    get_publisher_client,
    build_topic_path,
    publish_raw_message,
)
from messaging_models import EventMessage, BatchPublishResult, sanitize_event_attributes


def batch_publish(
    events: list[dict], default_event_type: str = "", default_source: str = ""
) -> BatchPublishResult:
    config = load_config()
    publisher = get_publisher_client()
    topic_path = build_topic_path(config)

    result = BatchPublishResult()

    for idx, event_data in enumerate(events):
        try:
            event_type = event_data.get("event_type", default_event_type) or "generic"
            source = event_data.get("source", default_source) or "batch-publish"

            event = EventMessage(
                event_type=event_type,
                source=source,
                payload=event_data.get("payload", event_data),
                attributes=event_data.get("attributes", {"batch_index": str(idx)}),
            )
            event.attributes["batch_id"] = event.attributes.get(
                "batch_id", str(uuid.uuid4())
            )

            payload_bytes = event.to_json().encode("utf-8")
            attributes = sanitize_event_attributes(
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "source": event.source,
                    "batch_index": str(idx),
                    **event.attributes,
                }
            )

            message_id = publish_raw_message(
                publisher, topic_path, payload_bytes, attributes
            )
            result.message_ids.append(message_id)
            result.published_count += 1

        except Exception as exc:
            result.failed_count += 1
            result.errors.append(
                {
                    "index": idx,
                    "error": str(exc),
                }
            )

    return result


if __name__ == "__main__":
    batch_events = [
        {
            "event_type": "user.signup",
            "source": "auth-service",
            "payload": {"user_id": "U001", "email": "a@example.com"},
        },
        {
            "event_type": "user.signup",
            "source": "auth-service",
            "payload": {"user_id": "U002", "email": "b@example.com"},
        },
        {
            "event_type": "user.signup",
            "source": "auth-service",
            "payload": {"user_id": "U003", "email": "c@example.com"},
        },
    ]
    result = batch_publish(batch_events)
    print(json.dumps(result.to_dict(), indent=2))
