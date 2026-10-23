import json
import os
from google.cloud import pubsub_v1


def consume_event(subscription_id=None, timeout=5.0):
    """Consume one message from Google Cloud Pub/Sub subscription."""
    if subscription_id is None:
        subscription_id = os.environ.get(
            "PUBSUB_SUBSCRIPTION_ID",
            "projects/my-project/subscriptions/my-subscription",
        )

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        "my-project", subscription_id.split("/")[-1]
    )

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
        data = json.loads(received_message.data.decode("utf-8"))
        return {
            "data": data,
            "message_id": received_message.message_id,
            "attributes": dict(received_message.attributes),
        }

    return None
