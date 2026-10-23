import os
import google.cloud.pubsub_v1 as pubsub

class MessagingClient:
    """Thin wrapper providing Pub/Sub publishing and consumption utilities.

    The class is instantiated once per process and reuses the underlying
    Pub/Sub client to avoid creating new connections on each call.
    """
    def __init__(self):
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        # Use default credentials from GOOGLE_APPLICATION_CREDENTIALS environment variable
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        self.project_id = project_id

    def publish_event(self, message: dict, topic_name: str) -> str:
        """Publish a single JSON event and return its Pub/Sub message ID."""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        data = json.dumps(message).encode('utf-8')
        future = self.publisher.publish(topic_path, data=data)
        try:
            msg_id = future.result()
            return msg_id
        except Exception as e:
            raise RuntimeError(f"Publish failed: {e}")

    def consume_event(self, subscription_name: str, callback) -> None:
        """Pull messages from a subscription using the supplied callback.

        The `callback` must accept a pubsub.PubsubMessage argument.
        """
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        with self.subscriber:
            self.subscriber.subscribe(subscription_path, callback=callback)
            # Blocking poll (in production you would likely run this in an async loop)
            self.subscriber.poll(timeout=None)

    def publish_batch(self, events: list[dict], topic_name: str) -> list[str]:
        """Publish a batch of events and return a list of IDs."""
        return batch_publish(events, self.project_id, topic_name)

    def dead_letter(self, original_message: dict, error_reason: str, dl_topic: str) -> None:
        """Republish a failed message to a dead‑letter topic."""
        dl_topic_path = self.publisher.topic_path(self.project_id, dl_topic)
        dl_payload = {**original_message, "error": error_reason}
        data = json.dumps(dl_payload).encode('utf-8')
        future = self.publisher.publish(dl_topic_path, data=data)
        try:
            future.result()
        except Exception as e:
            raise RuntimeError(f"Dead‑letter publish failed: {e}")
