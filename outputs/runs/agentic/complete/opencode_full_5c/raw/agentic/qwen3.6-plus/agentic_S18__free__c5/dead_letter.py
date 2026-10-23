import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import DeadLetterRequest, DeadLetterResponse


def send_to_dead_letter(
    original_message_id: str,
    original_data: dict,
    error_reason: str,
    retry_count: int = 0,
    attributes: dict = None,
) -> DeadLetterResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project")
    dlq_topic_id = os.environ.get("PUBSUB_DLQ_TOPIC_ID", "events-dead-letter")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, dlq_topic_id)

    request = DeadLetterRequest(
        original_message_id=original_message_id,
        original_data=original_data,
        error_reason=error_reason,
        retry_count=retry_count,
        attributes=attributes or {},
    )

    dlq_payload = json.dumps(request.to_dict()).encode("utf-8")

    dlq_attributes = {
        "dlq_reason": request.error_reason,
        "original_message_id": request.original_message_id,
        "retry_count": str(request.retry_count),
        "content_type": "application/json",
    }
    dlq_attributes.update(request.attributes)

    future = publisher.publish(topic_path, data=dlq_payload, **dlq_attributes)
    dlq_message_id = future.result()

    return DeadLetterResponse(
        dlq_message_id=dlq_message_id,
        original_message_id=request.original_message_id,
        dlq_topic_path=topic_path,
        status="routed_to_dead_letter",
        error_reason=request.error_reason,
    )


if __name__ == "__main__":
    failed_data = {"user_id": "usr_999", "action": "payment", "amount": -50}
    response = send_to_dead_letter(
        original_message_id="msg_abc123",
        original_data=failed_data,
        error_reason="validation_failed: negative amount",
        retry_count=3,
    )
    print(json.dumps(response.to_dict(), indent=2))
