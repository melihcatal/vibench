import os
import json
from google.cloud import pubsub_v1


def consume_event(subscription_id=None, timeout=5.0):
    """Consumes one message from a managed subscription or queue."""
    if subscription_id is None:
        subscription_id = os.environ.get(
            "PUBSUB_SUBSCRIPTION_ID",
            "projects/my-project/subscriptions/my-subscription",
        )

    subscriber = pubsub_v1.SubscriberClient()

    # Use a callback to process the message
    received_message = None
    ack_id = None

    def callback(message):
        nonlocal received_message, ack_id
        received_message = message.data.decode("utf-8")
        ack_id = message.ack_id
        message.ack()

    # Pull messages with streaming pull
    streaming_pull_future = subscriber.subscribe(subscription_id, callback)

    try:
        # Wait for a message to arrive
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    subscriber.close()

    if received_message:
        try:
            data = json.loads(received_message)
        except json.JSONDecodeError:
            data = received_message

        return {"data": data, "ack_id": ack_id, "subscription": subscription_id}
    return None


if __name__ == "__main__":
    message = consume_event()
    if message:
        print(f"Consumed message: {message['data']}")
    else:
        print("No messages available")
