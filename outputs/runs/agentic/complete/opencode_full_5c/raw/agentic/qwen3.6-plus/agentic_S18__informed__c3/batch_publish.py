import json
import os
from typing import Optional
from messaging_models import (
    PubSubEvent,
    BatchPublishResult,
    PublishResult,
    validate_event,
)
from messaging_client import topic_path, publish_message, validate_config


def publish_batch(
    events: list[PubSubEvent],
    max_retries: int = 3,
) -> BatchPublishResult:
    config_errors = validate_config()
    if config_errors:
        return BatchPublishResult(
            results=[
                PublishResult(
                    message_id="", success=False, error="; ".join(config_errors)
                )
                for _ in events
            ],
            total_sent=0,
            total_failed=len(events),
        )

    topic = topic_path()
    results = []
    total_sent = 0
    total_failed = 0

    for event in events:
        validation_errors = validate_event(event)
        if validation_errors:
            result = PublishResult(
                message_id="",
                success=False,
                error="; ".join(validation_errors),
            )
            results.append(result)
            total_failed += 1
            continue

        data = event.to_json().encode("utf-8")
        attributes = {
            "event_type": event.event_type,
            "source": event.source,
            "event_id": event.event_id,
            "batch": "true",
        }
        if event.correlation_id:
            attributes["correlation_id"] = event.correlation_id

        sent = False
        last_error = ""
        for attempt in range(max_retries):
            try:
                message_id = publish_message(topic, data, attributes)
                result = PublishResult(
                    message_id=message_id,
                    success=True,
                    topic=topic,
                )
                results.append(result)
                total_sent += 1
                sent = True
                break
            except Exception as exc:
                last_error = str(exc)
                continue

        if not sent:
            result = PublishResult(
                message_id="",
                success=False,
                error=last_error,
            )
            results.append(result)
            total_failed += 1

    return BatchPublishResult(
        results=results,
        total_sent=total_sent,
        total_failed=total_failed,
    )


def main():
    raw = os.environ.get(
        "BATCH_EVENTS",
        '[{"event_type":"order.created","source":"api","payload":{"order_id":"1"}},{"event_type":"order.updated","source":"api","payload":{"order_id":"2"}}]',
    )
    events_data = json.loads(raw)
    events = [PubSubEvent.from_dict(e) for e in events_data]
    result = publish_batch(events)
    print(json.dumps(result.to_dict(), default=str))


if __name__ == "__main__":
    main()
