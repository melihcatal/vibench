import os
from google.cloud import pubsub_v1

class PubSubClientHelper:
    """
    Provides helper utilities for interacting with Google Cloud Pub/Sub.
    Encapsulates client creation and project ID retrieval.
    """

    def __init__(self, project_id: str = None):
        self._project_id = project_id if project_id else os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self._project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")
        
        self._publisher_client = None
        self._subscriber_client = None

    def get_publisher_client(self) -> pubsub_v1.PublisherClient:
        """Returns a Pub/Sub PublisherClient instance."""
        if self._publisher_client is None:
            self._publisher_client = pubsub_v1.PublisherClient()
        return self._publisher_client

    def get_subscriber_client(self) -> pubsub_v1.SubscriberClient:
        """Returns a Pub/Sub SubscriberClient instance."""
        if self._subscriber_client is None:
            self._subscriber_client = pubsub_v1.SubscriberClient()
        return self._subscriber_client

    @property
    def project_id(self) -> str:
        """Returns the configured Google Cloud Project ID."""
        return self._project_id

    def get_topic_path(self, topic_id: str) -> str:
        """Constructs a fully qualified Pub/Sub topic path."""
        return self.get_publisher_client().topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Constructs a fully qualified Pub/Sub subscription path."""
        return self.get_subscriber_client().subscription_path(self.project_id, subscription_id)

