import os
from concurrent.futures import TimeoutError
from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import Message


def consume_event(subscription_id: str, timeout: float = 5.0) -> Message:
    """
    Consumes a single message from a Google Cloud Pub/Sub subscription.
    """
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_id)

    received_message = None

    def callback(message):
        nonlocal received_message
        print(f"Received message: {message.data.decode('utf-8')}")
        print(f"Attributes: {message.attributes}")
        received_message = Message(
            data=message.data,
            attributes=message.attributes,
            message_id=message.message_id,
        )
        message.ack()
        # Stop consuming after one message
        streaming_pull_future.cancel()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        print(f"No message received in {timeout} seconds.")

    subscriber.close()
    return received_message


if __name__ == "__main__":
    SUBSCRIPTION_ID = os.environ.get("GCP_SUBSCRIPTION_ID", "default-subscription")
    consume_event(SUBSCRIPTION_ID)
