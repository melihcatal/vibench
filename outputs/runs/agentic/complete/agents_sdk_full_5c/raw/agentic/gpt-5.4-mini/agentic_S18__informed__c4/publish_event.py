from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient
from messaging_models import PublishEventRequest


def publish_event(topic: str, payload: dict, attributes: dict | None = None, message_id: str | None = None):
    client = AzureServiceBusMessagingClient()
    request = PublishEventRequest(topic=topic, payload=payload, attributes=attributes or {}, message_id=message_id)
    return client.publish_event(request)
