import os
from google.cloud import pubsub_v1
from google.oauth2 import service_account

class PubSubClient:
    """Thin wrapper around Google Pub/Sub client library that consolidates credential handling.

    Uses GOOGLE_APPLICATION_CREDENTIALS env var for default auth, or accepts an explicit
    service account key via optional `json_key_path` argument.
    """
    def __init__(self, json_key_path: str | None = None):
        if json_key_path:
            credentials = service_account.Credentials.from_service_account_file(json_key_path)
            self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
            self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
        else:
            # Default client constructors will pick up GOOGLE_APPLICATION_CREDENTIALS
            self.publisher = pubsub_v1.PublisherClient()
            self.subscriber = pubsub_v1.SubscriberClient()

    def publish(self, topic_name: str, message: PubSubMessage) -> pubsub_v1.publisher.futures.Future:
        """Publish a single PubSubMessage.

        Args:
            topic_name (str): Fully qualified topic name.
            message (PubSubMessage): Wrapper containing bytes and optional attributes.
        """
        return self.publisher.publish(topic_name, message.data, **(message.attributes or {}))

    def publish_many(self, topic_name: str, messages: list[tuple[bytes, dict | None]]) -> list[pubsub_v1.publisher.futures.Future]:
        """Publish many messages in a single request.

        Args:
            topic_name (str): Fully qualified topic name.
            messages (list[tuple[bytes, dict]]): List of (data, attributes) pairs.
        """
        return self.publisher.publish_many(topic_name, messages)

    def subscribe(self, subscription_name: str, callback):
        """Begin asynchronous consumption from a subscription.

        Args:
            subscription_name (str): Fully qualified subscription name.
            callback (callable): Function accepting a PubsubMessage argument.
        """
        # The subscriber client uses its own credentials configured in init
        future = self.subscriber.subscribe(subscription_name, callback=callback)
        return future

    def ack(self, ack_id: str):
        """Acknowledge a previously pulled message.

        Args:
            ack_id (str): Ack ID returned with the message.
        """
        # Not a public method in client; provided for completeness when using low‑level API.
        pass

    def dead_letter(self, message: PubSubMessage, dlq_topic: str):
        """Delegate to the DeadLetter helper (implementation lives in dead_letter.py)."""
        from dead_letter import dead_letter
        dead_letter(message, dlq_topic)

    def __repr__(self):
        return "<PubSubClient using GOOGLE_APPLICATION_CREDENTIALS>"

# Simple immutable wrapper for a pulled Pub/Sub message
# This helps keep a consistent interface across local helpers and real SDK calls.
class PubSubMessage:
    def __init__(self, data: bytes, message_id: str | None = None, attributes: dict | None = None):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes
        self.ack_id = None  # Filled by low‑level pull responses when needed

    def ack(self):
        """Noop placeholder; real ack is performed by the subscriber client in the callback."""
        pass

    def __repr__(self):
        return f"PubSubMessage(id={self.message_id[:8]}... data_len={len(self.data)})"
