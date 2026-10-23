import os
from messaging_client import get_pubsub_client


def dead_letter(message, dlq_topic):
    """Send a failed message to a dead‑letter destination.

    Uses the same provider client as publish/consume.
    """
    client = get_pubsub_client()
    client.publish(dlq_topic, message.body)
    print(f"Moved failed message to dead‑letter topic {dlq_topic}")
