import os
from typing import List, Dict, Any, Optional

from google.cloud import pubsub_v1


class MessagingClient:
    """Local helper to abstract the concrete Google Cloud Pub/Sub provider.
    The client uses the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """

    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish(self, topic_name: str, message: Any) -> str:
        """Publish a single message and return the provider‑specific message ID."""
        topic_path = self.publisher.topic_path(os.getenv("PROJECT_ID"), topic_name)
        future = self.publisher.publish(
            topic_path, data=message.data, **message.attributes
        )
        # Block until the server acknowledges
        return future.result()

    def publish_batch(self, topic_name: str, messages: List[Any]) -> List[str]:
        """Publish a list of messages atomically and return a list of IDs."""
        topic_path = self.publisher.topic_path(os.getenv("PROJECT_ID"), topic_name)
        # The publish method returns a list of futures for batch publishing
        futures = self.publisher.publish(
            topic_path,
            messages=[msg.data for msg in messages],
            **{
                key: [msg.attributes.get(key, "") for msg in messages]
                for key in messages[0].attributes
            },
        )
        # Simplified: fetch all results synchronously
        return [f.result() for f in futures]

    def consume(self, subscription_name: str) -> Optional[Any]:
        """Consume a single message from the subscription."""
        subscription_path = self.subscriber.subscription_path(
            os.getenv("PROJECT_ID"), subscription_name
        )
        try:
            response = self.subscriber.pull(subscription_path, max_messages=1)
            if not response.received_messages:
                return None
            msg = response.received_messages[0].message
            # Acknowledge immediately after retrieval (simplified demo)
            self.subscriber.acknowledge(subscription_path, [msg.message_id])
            return msg
        except Exception:
            return None

    def __del__(self):
        self.publisher.close()
        self.subscriber.close()
