from google.cloud import pubsub_v1
import os

class PubSubClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.publisher_client = pubsub_v1.PublisherClient()
        self.subscriber_client = pubsub_v1.SubscriberClient()

    def get_publisher_client(self):
        return self.publisher_client

    def get_subscriber_client(self):
        return self.subscriber_client

    def topic_path(self, topic_id: str):
        return self.publisher_client.topic_path(self.project_id, topic_id)

    def subscription_path(self, subscription_id: str):
        return self.subscriber_client.subscription_path(self.project_id, subscription_id)
