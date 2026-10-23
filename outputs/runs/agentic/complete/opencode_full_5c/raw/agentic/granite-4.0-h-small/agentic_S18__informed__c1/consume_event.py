import json
from messaging_client import PubSubClient


def consume_event(subscription_name: str) -> dict:
    """Consume one message from the configured Pub/Sub subscription.

    Args:
        subscription_name: Name of the subscription to pull from.

    Returns:
        Dictionary representing the consumed message payload.
    """
    client = PubSubClient()
    # Pull a single message; provider-specific implementation inside client
    message = client.consume(subscription_name)
    if message is None:
        print(f"No message available on {subscription_name}")
        return {}
    # Decode JSON payload
    payload = json.loads(message.body)
    print(f"Consumed message from {subscription_name}: {payload}")
    return payload
