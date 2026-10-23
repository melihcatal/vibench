import os
import json
from google.cloud import pubsub_v1

class PubSubClient:
    def __init__(self, project_id=None, topic_id=None, subscription_id=None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.topic_id = topic_id or os.getenv("PUBSUB_TOPIC_ID")
        self.subscription_id = subscription_id or os.getenv("PUBSUB_SUBSCRIPTION_ID")

        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
        if not self.topic_id:
            raise ValueError("Pub/Sub Topic ID not provided and PUBSUB_TOPIC_ID environment variable not set.")
        if not self.subscription_id:
            raise ValueError("Pub/Sub Subscription ID not provided and PUBSUB_SUBSCRIPTION_ID environment variable not set.")

        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        self.subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)

    def publish_message(self, data, **attributes):
        if isinstance(data, dict):
            data = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            data = data.encode("utf-8")
        elif not isinstance(data, bytes):
            raise TypeError("Data must be bytes, string, or dict.")

        future = self.publisher.publish(self.topic_path, data, **attributes)
        return future.result()

    def subscribe_pull_messages(self, callback, max_messages=1):
        streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=callback)
        print(f"Listening for messages on {self.subscription_path}...")
        with self.subscriber:
            try:
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()

    def acknowledge_message(self, ack_id):
        self.subscriber.acknowledge(request={"subscription": self.subscription_path, "ack_ids": [ack_id]})

