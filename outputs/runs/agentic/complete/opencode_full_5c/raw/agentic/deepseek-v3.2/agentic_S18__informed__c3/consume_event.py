import os
import json
from google.cloud import pubsub_v1


def consume_event(subscription_name, timeout=5.0):
    """Consume one message from a Google Cloud Pub/Sub subscription."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    received_message = None

    def callback(message):
        nonlocal received_message
        received_message = message
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()

    if received_message:
        data = received_message.data.decode("utf-8")
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            payload = data

        return {
            "message_id": received_message.message_id,
            "data": payload,
            "attributes": dict(received_message.attributes),
            "publish_time": received_message.publish_time.isoformat(),
        }

    return None
