import os
from messaging_client import PubSubClient


def send_dead_letter(source_subscription, dlq_topic):
    """Move failed messages from a source subscription to a dead‑letter topic.

    Args:
        source_subscription (str): The subscription that produced the failure.
        dlq_topic (str): The dead‑letter topic where failures are stored.
    """
    client = PubSubClient()
    # Pull failed messages (assumes they are already in a dead‑letter pull subscription)
    message = client.pull(source_subscription)
    if not message:
        print(f"No failed messages to move.")
        return
    # Publish the payload to the DLQ topic
    client.publish(dlq_topic, message["data"])
    print(f"Moved failed message to dead‑letter topic {dlq_topic}")
