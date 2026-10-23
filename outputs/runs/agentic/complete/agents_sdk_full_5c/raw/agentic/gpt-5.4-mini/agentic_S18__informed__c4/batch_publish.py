from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient
from messaging_models import BatchPublishRequest, PublishEventRequest


def batch_publish(topic: str, messages: list[dict]):
    client = AzureServiceBusMessagingClient()
    items = [PublishEventRequest(topic=topic, payload=m["payload"], attributes=m.get("attributes", {}), message_id=m.get("message_id")) for m in messages]
    request = BatchPublishRequest(topic=topic, messages=items)
    return client.batch_publish(request)
