import json
from messaging_client import PubSubClient


def consume_event(subscription_id):
    """Consume a single message from a managed Pub/Sub subscription.

    Args:
        subscription_id (str): Identifier of the subscription to consume from.
    """
    client = PubSubClient()  # Google Cloud Pub/Sub provider
    message = client.pull(subscription_id)
    if message:
        payload = json.loads(message["data"])
        print(f"Consumed message: {payload}")
    else:
        print("No messages available. Check if subscription is correctly configured.")
