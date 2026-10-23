import json
import os
from messaging_models import PubSubMessage, DeadLetterResult
from messaging_client import dead_letter_topic_path, publish_message


def send_to_dead_letter(
    original_message: PubSubMessage,
    error_reason: str = "",
    retry_count: int = 0,
) -> DeadLetterResult:
    dl_topic = dead_letter_topic_path()
    original_payload = original_message.decode_payload()

    dead_letter_payload = json.dumps(
        {
            "original_message_id": original_message.message_id,
            "original_payload": original_payload,
            "original_attributes": original_message.attributes,
            "error_reason": error_reason,
            "retry_count": retry_count,
            "dead_letter_timestamp": __import__("datetime")
            .datetime.now(__import__("datetime").timezone.utc)
            .isoformat(),
        }
    ).encode("utf-8")

    attributes = {
        "original_message_id": original_message.message_id,
        "error_reason": error_reason[:256],
        "retry_count": str(retry_count),
        "dead_letter": "true",
    }

    try:
        dl_message_id = publish_message(dl_topic, dead_letter_payload, attributes)
        return DeadLetterResult(
            original_message_id=original_message.message_id,
            dead_letter_message_id=dl_message_id,
            success=True,
            retry_count=retry_count,
        )
    except Exception as exc:
        return DeadLetterResult(
            original_message_id=original_message.message_id,
            dead_letter_message_id="",
            success=False,
            error=str(exc),
            retry_count=retry_count,
        )


def main():
    sample_data = json.dumps({"test": "failed_event"}).encode("utf-8")
    msg = PubSubMessage(
        message_id="test-msg-001",
        data=sample_data,
        attributes={"event_type": "order.failed"},
    )
    result = send_to_dead_letter(
        msg, error_reason="Processing timeout exceeded", retry_count=3
    )
    print(json.dumps(result.to_dict(), default=str))


if __name__ == "__main__":
    main()
