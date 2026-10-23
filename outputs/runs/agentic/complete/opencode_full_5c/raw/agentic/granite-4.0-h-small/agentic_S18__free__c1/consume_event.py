import json
from messaging_client import MessagingClient


def consume_event(subscription_name: str) -> dict:
    """Consume a single message from a managed Pub/Sub subscription.

    Uses Google Cloud Pub/Sub as the concrete messaging provider.
    The provider is identifiable through the use of `subscriber.subscribe`
    and the `message.data` attribute of the received Pub/Sub message.
    """
    client = MessagingClient()
    subscription_path = (
        f"projects/{client.project_id}/subscriptions/{subscription_name}"
    )
    # Pull a single message (max_messages=1) with a short timeout
    messages = client.subscriber.subscribe(
        subscription_path, max_messages=1, timeout=10
    )
    for message in messages:
        # Decode the raw bytes payload to a string and then to dict
        payload = json.loads(message.data.decode("utf-8"))
        # Acknowledge the message after successful processing
        message.ack()
        print(f"Consumed message: {payload}")
        return payload
    raise ValueError("No messages available in subscription")
