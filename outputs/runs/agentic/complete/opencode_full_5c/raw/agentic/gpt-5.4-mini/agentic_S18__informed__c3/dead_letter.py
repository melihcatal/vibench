from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import encode_message, get_project_id, topic_path
from messaging_models import DeadLetterRequest, normalize_payload


def dead_letter(
    destination_topic: str,
    original_message_id: str,
    payload: Dict[str, Any],
    reason: str,
) -> str:
    project_id = get_project_id()
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    publisher = pubsub_v1.PublisherClient()
    request = DeadLetterRequest(
        destination=destination_topic,
        original_message_id=original_message_id,
        payload=normalize_payload(payload),
        reason=reason,
    )
    future = publisher.publish(
        topic_path(project_id, request.destination),
        encode_message(request.payload),
        original_message_id=request.original_message_id,
        dead_letter_reason=request.reason,
    )
    return future.result()
