from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient
from messaging_models import DeadLetterRecord


def dead_letter(destination: str, source_subscription: str, reason: str, payload: dict, attributes: dict | None = None):
    client = AzureServiceBusMessagingClient()
    record = DeadLetterRecord(source_subscription=source_subscription, reason=reason, payload=payload, attributes=attributes or {})
    return client.send_dead_letter(destination, record)
