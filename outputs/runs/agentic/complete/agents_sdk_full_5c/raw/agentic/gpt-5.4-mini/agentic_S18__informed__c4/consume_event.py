from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient


def consume_event(subscription: str):
    client = AzureServiceBusMessagingClient()
    return client.consume_one(subscription)
