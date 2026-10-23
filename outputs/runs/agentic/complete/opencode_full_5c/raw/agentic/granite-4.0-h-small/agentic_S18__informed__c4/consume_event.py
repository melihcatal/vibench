import os
from messaging_client import get_sub_client


def consume_event(subscription_name):
    """Consume a single message from the configured subscription.

    Uses the active provider's client (e.g., AWS SQS, GCP Pub/Sub, Azure Service Bus)."
    """
    client = get_sub_client()
    message = client.receive(subscription_name)
    if message:
        payload = message.body
        print(f"Consumed message: {payload}")
        # Acknowledge/delete as required by the provider
        client.acknowledge(message)
    else:
        print("No message available.")
