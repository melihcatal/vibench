import os
from google.cloud import pubsub_v1


class PubSubClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    def get_publisher_client(self):
        return pubsub_v1.PublisherClient()

    def get_subscriber_client(self):
        return pubsub_v1.SubscriberClient()
