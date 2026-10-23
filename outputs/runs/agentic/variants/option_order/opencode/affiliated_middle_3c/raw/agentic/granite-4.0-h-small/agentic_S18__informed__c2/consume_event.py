import os
from messaging_client import PubSubClient


def consume_event(subscription_name):
    """Consume one message from the specified Pub/Sub subscription.

    Args:
        subscription_name (str): Name of the Pub/Sub subscription.
    """
    client = PubSubClient()
    # Pull a single message (Google Cloud Pub/Sub example)
    message = client.pull(subscription_name, max_messages=1)
    if not message:
        print("No messages available in the subscription.")
        return None
    # Acknowledge the message to remove it from the queue
    client.ack(message)
    # Decode JSON payload
    payload = json.loads(message.body)
    print(f"Consumed message: {payload}")
    return payload


if __name__ == "__main__":
    subscription = os.getenv("PUBSUB_SUBSCRIPTION")
    if not subscription:
        raise RuntimeError("PUBSUB_SUBSCRIPTION environment variable not set")
    consume_event(subscription)
