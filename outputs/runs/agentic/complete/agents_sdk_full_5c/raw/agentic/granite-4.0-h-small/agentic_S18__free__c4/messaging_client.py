import os
from google.cloud import pubsub_v1

# Configuration provider-detection helpers
IS_GOOGLE_CLOUD = os.getenv('K_SERVICE') is not None  # Cloud Run / Cloud Functions signal

class PubSubClient:
    """Helper wrapper for Google Cloud Pub/Sub client."""
    def __init__(self, project_id: str, topic_id: str = None, subscription_id: str = None):
        self.project_id = project_id
        self.topic_path = None
        self.subscription_path = None
        self.publisher = None
        self.topic_id = topic_id
        self.subscription_id = subscription_id
        self._initialize_clients()

    def _initialize_clients(self):
        self.publisher = pubsub_v1.PublisherClient()
        if self.topic_id:
            self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        if self.subscription_id:
            self.subscription_path = self.publisher.subscription_path(self.project_id, self.subscription_id)

    @property
    def subscription_path(self):
        if not hasattr(self, '_subscription_path'):
            self._subscription_path = self.publisher.subscription_path(self.project_id, self.subscription_id)
        return self._subscription_path

    @property
    def topic_path(self):
        if not hasattr(self, '_topic_path'):
            self._topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        return self._topic_path

    def publish(self, *, topic_path: str = None, data: bytes, **kwargs):
        """Publish a single message."""
        if topic_path is None:
            topic_path = self.topic_path
        return self.publisher.publish(topic_path, data, **kwargs)

    def pull(self, *, max_messages: int = 1):
        """Pull messages using the subscriber client."""
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(self.project_id, self.subscription_id)
        response = subscriber.pull(request={'subscription': subscription_path, 'max_messages': max_messages})
        return response
