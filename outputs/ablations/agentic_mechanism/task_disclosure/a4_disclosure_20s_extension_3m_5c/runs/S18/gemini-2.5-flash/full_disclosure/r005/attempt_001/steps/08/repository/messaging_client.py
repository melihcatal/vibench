import os
from google.cloud import pubsub_v1

class PubSubClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_publisher_client(self):
        return self.publisher

    def get_subscriber_client(self):
        return self.subscriber

    def get_project_id(self):
        return self.project_id
