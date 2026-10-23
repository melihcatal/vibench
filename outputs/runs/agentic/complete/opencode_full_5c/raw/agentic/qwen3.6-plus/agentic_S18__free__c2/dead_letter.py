from google.cloud.pubsub_v1 import PublisherClient

from messaging_client import (
    create_publisher_client,
    get_dead_letter_topic_path,
    ensure_topic_exists,
)
from messaging_models import DeadLetterResult


def send_to_dead_letter(
    original_message_id: str,
    original_payload: str,
    failure_reason: str,
    retry_count: int = 0,
    original_attributes: dict | None = None,
) -> DeadLetterResult:
    publisher: PublisherClient = create_publisher_client()
    dead_letter_topic_path = get_dead_letter_topic_path()
    ensure_topic_exists(publisher, dead_letter_topic_path)

    dead_letter_payload = {
        "original_message_id": original_message_id,
        "original_payload": original_payload,
        "failure_reason": failure_reason,
        "retry_count": retry_count,
        "dead_lettered_at": True,
    }

    payload_bytes = str(dead_letter_payload).encode("utf-8")

    attributes = {
        "original_message_id": original_message_id,
        "failure_reason": failure_reason,
        "retry_count": str(retry_count),
        "dead_letter_status": "failed",
    }
    if original_attributes:
        for k, v in original_attributes.items():
            attributes[f"orig_{k}"] = str(v)

    future = publisher.publish(
        topic=dead_letter_topic_path,
        data=payload_bytes,
        **attributes,
    )
    dead_letter_message_id = future.result()

    return DeadLetterResult(
        original_message_id=original_message_id,
        dead_letter_message_id=dead_letter_message_id,
        failure_reason=failure_reason,
        retry_count=retry_count,
        status="dead_lettered",
    )


if __name__ == "__main__":
    import json
    import sys

    raw = (
        sys.stdin.read()
        if not sys.stdin.isatty()
        else '{"original_message_id":"msg-123","original_payload":"{"data":"test"}","failure_reason":"processing_timeout","retry_count":3}'
    )
    data = json.loads(raw)
    result = send_to_dead_letter(
        original_message_id=data["original_message_id"],
        original_payload=data["original_payload"],
        failure_reason=data["failure_reason"],
        retry_count=data.get("retry_count", 0),
        original_attributes=data.get("original_attributes"),
    )
    print(json.dumps(result.to_dict()))
