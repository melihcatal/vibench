import os
from google.cloud import pubsub_v1

class PubSubClient:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

        self.publisher_client = pubsub_v1.PublisherClient()
        self.subscriber_client = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        return self.publisher_client.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        return self.subscriber_client.subscription_path(self.project_id, subscription_id)

    def get_publisher_client(self):
        return self.publisher_client

    def get_subscriber_client(self):
        return self.subscriber_client
