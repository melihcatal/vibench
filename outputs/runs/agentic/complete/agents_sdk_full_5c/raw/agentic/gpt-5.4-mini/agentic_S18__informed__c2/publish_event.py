from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient
from messaging_models import MessageEnvelope, normalize_payload


def publish_event(event_type: str, payload: dict | str, **attributes: str):
    client = AzureServiceBusMessagingClient()
    envelope = MessageEnvelope(event_type=event_type, payload=normalize_payload(payload), attributes=attributes)
    return client.publish_event(envelope)
