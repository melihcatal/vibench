import os
from google.cloud import pubsub_v1

class PubSubClientHelper:
    def __init__(self):
        self.project_id = os.environ.get("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    def get_publisher_client(self) -> pubsub_v1.PublisherClient:
        return self.publisher

    def get_subscriber_client(self) -> pubsub_v1.SubscriberClient:
        return self.subscriber
