import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError, RetryError

class PubSubClient:
    """High-level client wrapper for Google Pub/Sub."""
    def __init__(self, project_id=None):
        self.project_id = project_id or os.getenv('PUBSUB_PROJECT_ID')
        if not self.project_id:
            raise RuntimeError('PUBSUB_PROJECT_ID environment variable not set')
        # Create low-level client once
        self._publisher = pubsub_v1.PublisherClient()
        self._subscriber = pubsub_v1.SubscriberClient()

    def publish(self, topic_id, message):
        """Publish a single or list of messages to a topic."""
        topic_path = self._publisher.topic_path(self.project_id, topic_id)
        # Pub/Sub expects a list of dict-encoded messages
        if not isinstance(message, (list, tuple)):
            message = [message]
        # The PublisherClient expects a dict that will be serialized by protobuf
        # Here we just forward the dict; underlying client will encode it.
        try:
            response = self._publisher.publish(topic_path, **message)
            return response
        except (GoogleAPICallError, RetryError) as exc:
            print(f'Publish failed: {exc}')
            raise

    def pull(self, subscription_id, max_messages=1):
        """Pull up to max_messages from a subscription."""
        subscription_path = self._subscriber.subscription_path(self.project_id, subscription_id)
        try:
            # pull() is a streaming call; we use next() to get the first response
            future = self._subscriber.pull(subscription_path, max_messages=max_messages, timeout=10)
            # The pull response comes as an iterable of ReceivedMessage objects
            list_of_received = list(future.result(timeout=5))
            return pubsub_v1.types.PullResponse(received_messages=list_of_received)
        except GoogleAPICallError as exc:
            print(f'Pull failed: {exc}')
            raise

    def acknowledge(self, subscription_id, ack_id):
        """Acknowledge a pulled message."""
        subscription_path = self._subscriber.subscription_path(self.project_id, subscription_id)
        self._subscriber.acknowledge(subscription_path, [ack_id])
