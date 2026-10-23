import os
from google.cloud import pubsub_v1
from typing import Optional


class PubSubClient:
    def __init__(self, project_id: Optional[str] = None):
        if project_id is None:
            self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if not self.project_id:
                raise ValueError(
                    "GOOGLE_CLOUD_PROJECT environment variable not set and no project_id provided."
                )
        else:
            self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        return self.subscriber.subscription_path(self.project_id, subscription_id)
