import os
from google.cloud import pubsub_v1

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
subscription_id = "your-subscription-id"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def consume_event(callback):
    def callback_wrapper(message):
        callback(message.data)
        message.ack()

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback_wrapper
    )
    print(f"Listening for messages on {subscription_path}...")
    streaming_pull_future.result()
