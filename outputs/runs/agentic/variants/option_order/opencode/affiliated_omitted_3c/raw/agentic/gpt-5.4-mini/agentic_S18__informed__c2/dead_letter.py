import json

from google.cloud import pubsub_v1

from messaging_client import get_pubsub_client, topic_path
from messaging_models import DeadLetterRequest, normalize_message_payload


def send_dead_letter(
    destination: str, original_message_id, payload, reason: str
) -> str:
    client = get_pubsub_client()
    request = DeadLetterRequest(
        destination=destination,
        original_message_id=original_message_id,
        payload=normalize_message_payload(payload),
        reason=reason,
    )
    data = json.dumps(
        {
            "original_message_id": request.original_message_id,
            "payload": request.payload,
            "reason": request.reason,
        },
        separators=(",", ":"),
    ).encode("utf-8")
    future = client.publish(
        topic_path(request.destination), data, dead_letter_reason=request.reason
    )
    return future.result()
