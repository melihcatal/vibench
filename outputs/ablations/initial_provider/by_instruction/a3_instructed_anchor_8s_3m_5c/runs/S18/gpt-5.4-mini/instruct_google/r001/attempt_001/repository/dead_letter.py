import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import publisher_client, topic_path
from messaging_models import DeadLetterRequest, normalize_payload


def send_dead_letter(destination: str, original_message: Dict[str, Any], reason: str) -> Dict[str, Any]:
    client = publisher_client()
    request = DeadLetterRequest(destination=topic_path(destination), original_message=normalize_payload(original_message), reason=reason)
    payload = {"original_message": request.original_message, "reason": request.reason}
    message_id = client.publish(request.destination, json.dumps(payload).encode("utf-8"), dead_letter_reason=reason).result()
    return {"message_id": message_id, "destination": request.destination}
