import os
import json
from google.cloud import pubsub_v1


def consume_event(subscription_id=None, timeout=5.0):
    """Consume one message from Google Cloud Pub/Sub subscription."""
    if subscription_id is None:
        subscription_id = os.getenv("PUBSUB_SUBSCRIPTION_ID", "event-subscription")

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    received_message = None

    def callback(message):
        nonlocal received_message
        received_message = {
            "data": message.data.decode("utf-8"),
            "message_id": message.message_id,
            "attributes": message.attributes,
            "publish_time": message.publish_time,
        }
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()

    streaming_pull_future.cancel()

    if received_message:
        try:
            received_message["data"] = json.loads(received_message["data"])
        except json.JSONDecodeError:
            pass

    return received_message
