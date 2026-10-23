import os
from google.cloud import pubsub_v1
from typing import Optional


class PubSubClient:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable is required.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        topic_id = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
        self.topic_path = self.publisher.topic_path(self.project_id, topic_id)
        sub_id = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
        self.subscription_path = self.subscriber.subscription_path(
            self.project_id, sub_id
        )
        dl_topic_id = os.getenv("DEAD_LETTER_TOPIC_ID", "dead-letter-topic")
        self.dead_letter_topic_path = self.publisher.topic_path(
            self.project_id, dl_topic_id
        )
