from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_subscriber, subscription_path
from messaging_models import ConsumeRequest, IntegrationResponse


def consume_event(project_id: str, subscription_name: str, max_messages: int = 1) -> IntegrationResponse:
    project_id = get_project_id(project_id)
    subscriber: pubsub_v1.SubscriberClient = get_subscriber(project_id)
    request = ConsumeRequest(subscription_path=subscription_path(project_id, subscription_name), max_messages=max_messages)
    response = subscriber.pull(subscription=request.subscription_path, max_messages=request.max_messages, return_immediately=True)
    if not response.received_messages:
        return IntegrationResponse(provider="google_pubsub", resource=request.subscription_path, details={"messages": []})
    received = response.received_messages[0]
    subscriber.acknowledge(subscription=request.subscription_path, ack_ids=[received.ack_id])
    return IntegrationResponse(provider="google_pubsub", resource=request.subscription_path, message_ids=[received.message.message_id], message={"data": received.message.data.decode("utf-8")}, details={"attributes": dict(received.message.attributes)})
