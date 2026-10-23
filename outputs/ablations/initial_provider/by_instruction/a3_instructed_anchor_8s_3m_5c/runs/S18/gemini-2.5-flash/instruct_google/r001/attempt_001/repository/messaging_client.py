from google.cloud import pubsub_v1
import os

class PubSubClient:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_publisher_client(self):
        return self.publisher

    def get_subscriber_client(self):
        return self.subscriber

    def topic_path(self, topic_id: str):
        return self.publisher.topic_path(self.project_id, topic_id)

    def subscription_path(self, subscription_id: str):
        return self.subscriber.subscription_path(self.project_id, subscription_id)
