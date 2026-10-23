from google.cloud import pubsub_v1
from messaging_client import (
    get_publisher_client,
    get_subscriber_client,
    topic_path,
    subscription_path,
    load_topic_config,
    build_publish_request,
)
from messaging_models import PubSubEvent, DeadLetterResult, ConsumeResult


def send_to_dead_letter(
    consume_result: ConsumeResult,
    failure_reason: str,
    dead_letter_topic_name: str | None = None,
) -> DeadLetterResult:
    config = load_topic_config()
    project_id = config["project_id"]
    dl_topic_name = dead_letter_topic_name or config["dead_letter_topic"]
    dl_topic = topic_path(project_id, dl_topic_name)
    publisher = get_publisher_client()

    event = consume_result.to_event()
    if event is None and consume_result.raw_data:
        event = PubSubEvent.from_json(consume_result.raw_data)

    dead_letter_payload = {
        "original_message_id": consume_result.message_id,
        "failure_reason": failure_reason,
        "redelivery_count": consume_result.delivery_attempt,
        "original_event": event.to_json() if event else consume_result.raw_data,
    }

    dl_event = PubSubEvent(
        event_type="message.dead_lettered",
        source="dead-letter-handler",
        payload=dead_letter_payload,
        attributes={
            "original_message_id": consume_result.message_id,
            "failure_reason": failure_reason,
        },
    )

    attrs = {
        "event_type": dl_event.event_type,
        "original_message_id": consume_result.message_id,
        "failure_reason": failure_reason,
    }
    request = build_publish_request(dl_event.to_json().encode("utf-8"), attrs)
    future = publisher.publish(dl_topic, **request)
    dl_message_id = future.result()

    return DeadLetterResult(
        original_message_id=consume_result.message_id,
        dead_letter_message_id=dl_message_id,
        dead_letter_topic=dl_topic,
        failure_reason=failure_reason,
        redelivery_count=consume_result.delivery_attempt,
    )


if __name__ == "__main__":
    cr = ConsumeResult(
        message_id="msg-failed-001",
        raw_data='{"event_id": "evt-001", "event_type": "test", "source": "test", "timestamp": "2024-01-01T00:00:00Z", "payload": {}, "attributes": {}}',
        delivery_attempt=3,
    )
    result = send_to_dead_letter(
        cr, "Payload validation failed: missing required field"
    )
    print(result.to_dict())
