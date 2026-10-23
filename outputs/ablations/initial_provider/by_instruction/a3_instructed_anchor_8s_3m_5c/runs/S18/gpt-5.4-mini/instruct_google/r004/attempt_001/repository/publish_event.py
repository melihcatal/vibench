import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher, get_project_id, topic_path
from messaging_models import IntegrationResponse, PublishRequest, normalize_attributes, normalize_payload


def publish_event(project_id: str, topic_name: str, event, attributes=None) -> IntegrationResponse:
    project_id = get_project_id(project_id)
    publisher: pubsub_v1.PublisherClient = get_publisher(project_id)
    request = PublishRequest(topic_path=topic_path(project_id, topic_name), event=normalize_payload(event), attributes=normalize_attributes(attributes))
    data = json.dumps(request.event).encode("utf-8")
    future = publisher.publish(request.topic_path, data, **request.attributes)
    message_id = future.result()
    return IntegrationResponse(provider="google_pubsub", resource=request.topic_path, message_ids=[message_id], message=request.event)
