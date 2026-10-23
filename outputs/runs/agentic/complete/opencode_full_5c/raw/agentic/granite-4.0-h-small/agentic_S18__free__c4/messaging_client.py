import os
from google.cloud import (
    pubsub_v1,
)  # concrete Google Cloud Pub/Sub SDK import (provider identifier)


class PubSubClient:
    """Helper client for Google Cloud Pub/Sub publish/subscribe operations."""

    def __init__(self):
        # Use GOOGLE_APPLICATION_CREDENTIALS env var for auth (provider‑specific auth)
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish(self, topic_id, data):
        """Publish a single JSON message."""
        future = self.publisher.publish(topic_id, data.encode("utf-8"))
        return future.result()

    def publish_batch(self, topic_id, data_list):
        """Publish a list of JSON messages in a batch."""
        futures = [
            self.publisher.publish(topic_id, d.encode("utf-8")) for d in data_list
        ]
        return [f.result() for f in futures]

    def pull(self, subscription_id):
        """Pull a single message (sync call)."""
        response = self.subscriber.pull(subscription_id, max_messages=1)
        if response.message_bytes:
            msg = response.message_bytes[0]
            return {
                "data": msg.message.data,
                "attributes": msg.message.attributes,
                "message_id": msg.message_id,
            }
        return None
