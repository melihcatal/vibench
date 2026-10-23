import os
from datetime import datetime, timezone

from google.cloud import pubsub_v1

from messaging_client import (
    get_project_id,
    get_pubsub_publisher_client,
    topic_path,
    load_topic_config,
)
from messaging_models import DeadLetterResult


def send_to_dead_letter(
    original_message_id: str,
    event_data: bytes,
    failure_reason: str,
    retry_count: int,
    attributes: dict | None = None,
    dead_letter_topic_name: str | None = None,
    project_id: str | None = None,
) -> DeadLetterResult:
    project_id = project_id or get_project_id()
    config = load_topic_config()
    dead_letter_topic_name = dead_letter_topic_name or config["dead_letter_topic_name"]

    publisher = get_pubsub_publisher_client()
    dl_topic = topic_path(project_id, dead_letter_topic_name)

    dl_attributes = {
        "original_message_id": original_message_id,
        "failure_reason": failure_reason,
        "retry_count": str(retry_count),
        "dead_lettered_at": datetime.now(timezone.utc).isoformat(),
    }
    if attributes:
        dl_attributes.update({k: str(v) for k, v in attributes.items()})

    future = publisher.publish(
        dl_topic,
        data=event_data,
        **dl_attributes,
    )
    dead_letter_message_id = future.result()

    return DeadLetterResult(
        original_message_id=original_message_id,
        dead_letter_message_id=dead_letter_message_id,
        failure_reason=failure_reason,
        retry_count=retry_count,
        timestamp=dl_attributes["dead_lettered_at"],
    )


def handle_failed_message(
    consume_result,
    failure_reason: str,
    project_id: str | None = None,
) -> DeadLetterResult:
    config = load_topic_config()
    max_attempts = config["max_delivery_attempts"]

    if consume_result.delivery_attempt >= max_attempts:
        return send_to_dead_letter(
            original_message_id=consume_result.message_id,
            event_data=consume_result.event.to_pubsub_data(),
            failure_reason=failure_reason,
            retry_count=consume_result.delivery_attempt,
            attributes={
                "event_type": consume_result.event.event_type,
                "source": consume_result.event.source,
            },
            project_id=project_id,
        )
    raise RuntimeError(
        f"Message {consume_result.message_id} has {consume_result.delivery_attempt} "
        f"attempts, below threshold of {max_attempts}"
    )


if __name__ == "__main__":
    from messaging_models import EventMessage

    event = EventMessage.create(
        "payment.failed", "payment-service", {"error": "timeout"}
    )
    result = send_to_dead_letter(
        original_message_id="msg-001",
        event_data=event.to_pubsub_data(),
        failure_reason="Processing timeout after 5 retries",
        retry_count=5,
    )
    print(result.to_dict())
