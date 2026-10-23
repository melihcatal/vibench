import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher, get_project_id, topic_path
from messaging_models import DeadLetterRequest, IntegrationResponse, normalize_payload


def dead_letter_message(project_id: str, topic_name: str, failed_message, reason: str) -> IntegrationResponse:
    project_id = get_project_id(project_id)
    publisher: pubsub_v1.PublisherClient = get_publisher(project_id)
    request = DeadLetterRequest(topic_path=topic_path(project_id, topic_name), failed_message=normalize_payload(failed_message), reason=reason)
    payload = {"reason": request.reason, "failed_message": request.failed_message}
    message_id = publisher.publish(request.topic_path, json.dumps(payload).encode("utf-8"), dead_letter_reason=request.reason).result()
    return IntegrationResponse(provider="google_pubsub", resource=request.topic_path, message_ids=[message_id], message=payload)
