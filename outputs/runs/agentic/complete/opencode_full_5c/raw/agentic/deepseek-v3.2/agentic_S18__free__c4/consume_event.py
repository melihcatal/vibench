import json
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError


def consume_event(subscription_id=None, timeout=5.0):
    """Consume one message from Google Cloud Pub/Sub subscription."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if subscription_id is None:
        subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "event-subscription")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    received_message = None
    ack_id = None

    def callback(message):
        nonlocal received_message, ack_id
        received_message = message
        ack_id = message.ack_id
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()

    if received_message:
        try:
            data = json.loads(received_message.data.decode("utf-8"))
        except:
            data = received_message.data.decode("utf-8")

        return {
            "message_id": received_message.message_id,
            "data": data,
            "attributes": dict(received_message.attributes),
            "publish_time": received_message.publish_time.isoformat(),
            "ack_id": ack_id,
            "provider": "google-cloud-pubsub",
        }

    return None


if __name__ == "__main__":
    message = consume_event()
    if message:
        print(f"Consumed message: {message}")
    else:
        print("No messages available")
