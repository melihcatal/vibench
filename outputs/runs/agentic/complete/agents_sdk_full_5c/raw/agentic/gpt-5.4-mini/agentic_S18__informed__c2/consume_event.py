from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient
from messaging_models import ProcessedMessage


def consume_event() -> ProcessedMessage | None:
    client = AzureServiceBusMessagingClient()
    raw = client.consume_one()
    if raw is None:
        return None
    return ProcessedMessage.from_mapping(raw)
