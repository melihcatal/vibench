import os
from messaging_client import PubSubClient


def send_dead_letter(source_subscription: str, dlq_topic: str, message_id: str):
    """Move a failed message to a dead-letter topic/queue.

    Uses Alibaba Cloud MNS (RocketMQ) SDK for demonstration.
    Requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET env vars.
    """
    client = PubSubClient()
    # Retrieve the failed message (placeholder - actual retrieval may vary by provider)
    failed_message = client.fetch_failed_message(source_subscription, message_id)
    if not failed_message:
        print("Failed message not found.")
        return
    # Publish to dead-letter destination
    client.publish(dlq_topic, failed_message)
    print(f"Dead-lettered message {message_id} to topic '{dlq_topic}'.")
