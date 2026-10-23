from messaging_client import PubSubClient
from messaging_models import ConsumeResponse
import os


def consume_event(subscription_id: str, timeout: float = 10.0) -> ConsumeResponse:
    """
    Consumes one message from a Google Cloud Pub/Sub subscription.
    """
    client = PubSubClient()
    message = client.pull_message(subscription_id, timeout)
    return ConsumeResponse(message=message)


if __name__ == "__main__":
    subscription_id = os.getenv("PUBSUB_SUBSCRIPTION_ID")
    response = consume_event(subscription_id)
    if response.message:
        print(f"Consumed message: {response.message}")
    else:
        print("No messages available.")
