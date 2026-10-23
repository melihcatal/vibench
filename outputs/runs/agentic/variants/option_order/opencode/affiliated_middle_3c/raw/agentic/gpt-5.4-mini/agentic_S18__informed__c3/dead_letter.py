from messaging_client import get_publisher, topic_path
from messaging_models import (
    MessageRequest,
    MessageResponse,
    normalize_attributes,
    normalize_payload,
)


def send_to_dead_letter(
    topic: str, failed_payload: str, reason: str, attributes: dict | None = None
) -> MessageResponse:
    merged = normalize_attributes(attributes)
    merged["dead_letter_reason"] = reason
    publisher = get_publisher()
    future = publisher.publish(
        topic_path(topic),
        data=normalize_payload(failed_payload).encode("utf-8"),
        **merged,
    )
    return MessageResponse(
        message_id=future.result(), status="dead_lettered", attributes=merged
    )
