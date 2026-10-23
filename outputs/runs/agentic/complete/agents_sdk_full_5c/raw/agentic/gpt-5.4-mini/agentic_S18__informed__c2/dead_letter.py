from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient


def send_dead_letter(body, reason: str, description: str = "message processing failed"):
    client = AzureServiceBusMessagingClient()
    return client.dead_letter(reason=reason, description=description, body=body)
