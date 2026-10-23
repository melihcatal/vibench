from google.cloud import pubsub_v1
import os
from typing import Optional

# Provider: Google Cloud Pub/Sub
# Identifiable by: google.cloud.pubsub_v1, GOOGLE_APPLICATION_CREDENTIALS


class MessagingClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_publisher(self) -> pubsub_v1.PublisherClient:
        return self.publisher

    def get_subscriber(self) -> pubsub_v1.SubscriberClient:
        return self.subscriber

    def get_topic_path(self, topic_name: str) -> str:
        return self.publisher.topic_path(self.project_id, topic_name)

    def get_subscription_path(self, subscription_name: str) -> str:
        return self.subscriber.subscription_path(self.project_id, subscription_name)
