import os
from google.cloud import pubsub_v1  # Example provider: Google Cloud Pub/Sub


class PubSubClient:
    """Local helper client wrapping Google Cloud Pub/Sub operations."""

    def __init__(self):
        # Use application default credentials (env var) for auth
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        # Topics and subscriptions are assumed to be pre‑created
        self.project = os.getenv("GOOGLE_CLOUD_PROJECT") or "your-project-id"

    def publish(self, topic_name, payload):
        """Publish a single message or a list of messages.
        If payload is a list, each element is sent as an individual publish request.
        """
        topic_path = f"projects/{self.project}/topics/{topic_name}"
        if isinstance(payload, list):
            # Simple loop‑based batch publish (synchronous)
            for p in payload:
                self.publisher.publish(topic_path, data=p.encode()).result()
        else:
            self.publisher.publish(topic_path, data=payload.encode()).result()
        return f"Published to {topic_path}"

    def pull(self, subscription_name, max_messages=1):
        """Pull a single message (or up to max_messages) from a subscription."""
        subscription_path = f"projects/{self.project}/subscriptions/{subscription_name}"
        response = self.subscriber.pull(
            subscription_path, max_messages=max_messages, timeout=10
        )
        if not response.received_messages:
            return None
        # Return first message for simplicity
        msg = response.received_messages[0]
        return msg.message

    def ack(self, message):
        """Acknowledge a pulled message."""
        self.subscriber.acknowledge(
            f"projects/{self.project}/subscriptions/{message.subscription}",
            [message.ack_id],
        )
