import os
from google.cloud import pubsub_v1


def consume_event(subscription_name):
    project_id = "your-project-id"
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print(f"Received message: {message.data}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    streaming_pull_future.result()
