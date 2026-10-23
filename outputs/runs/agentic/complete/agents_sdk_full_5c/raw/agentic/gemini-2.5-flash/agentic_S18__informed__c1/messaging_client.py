import os
from google.cloud import pubsub_v1

class PubSubClientHelper:
    def __init__(self, project_id: str = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self._publisher_client = None
        self._subscriber_client = None

    @property
    def publisher_client(self) -> pubsub_v1.PublisherClient:
        if self._publisher_client is None:
            self._publisher_client = pubsub_v1.PublisherClient()
        return self._publisher_client

    @property
    def subscriber_client(self) -> pubsub_v1.SubscriberClient:
        if self._subscriber_client is None:
            self._subscriber_client = pubsub_v1.SubscriberClient()
        return self._subscriber_client

    def get_topic_path(self, topic_id: str) -> str:
        return self.publisher_client.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        return self.subscriber_client.subscription_path(self.project_id, subscription_id)

    def close_clients(self):
        if self._publisher_client:
            self._publisher_client.close()
        if self._subscriber_client:
            self._subscriber_client.close()
