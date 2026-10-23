import os
from google.cloud import pubsub_v1


class PubSubClient:
    """Manages Google Cloud Pub/Sub client and related configurations."""

    def __init__(self, project_id: Optional[str] = None):
        if project_id is None:
            self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if not self.project_id:
                raise ValueError(
                    "Google Cloud Project ID not found. Please set GOOGLE_CLOUD_PROJECT environment variable."
                )
        else:
            self.project_id = project_id

        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        """Returns the full topic path for a given topic ID."""
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Returns the full subscription path for a given subscription ID."""
        return self.subscriber.subscription_path(self.project_id, subscription_id)
