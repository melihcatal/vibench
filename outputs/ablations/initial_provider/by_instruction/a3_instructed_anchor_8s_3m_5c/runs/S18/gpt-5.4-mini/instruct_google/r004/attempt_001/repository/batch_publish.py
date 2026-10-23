import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher, get_project_id, topic_path
from messaging_models import BatchPublishRequest, IntegrationResponse, normalize_attributes, normalize_payload


def batch_publish(project_id: str, topic_name: str, messages):
    project_id = get_project_id(project_id)
    publisher: pubsub_v1.PublisherClient = get_publisher(project_id)
    request = BatchPublishRequest(topic_path=topic_path(project_id, topic_name), messages=messages)
    message_ids = []
    normalized_messages = []
    for message in request.messages:
        payload = normalize_payload(message.get("payload") or message.get("event") or message)
        attrs = normalize_attributes(message.get("attributes"))
        message_ids.append(publisher.publish(request.topic_path, json.dumps(payload).encode("utf-8"), **attrs).result())
        normalized_messages.append({"payload": payload, "attributes": attrs})
    return IntegrationResponse(provider="google_pubsub", resource=request.topic_path, message_ids=message_ids, details={"messages": normalized_messages})
