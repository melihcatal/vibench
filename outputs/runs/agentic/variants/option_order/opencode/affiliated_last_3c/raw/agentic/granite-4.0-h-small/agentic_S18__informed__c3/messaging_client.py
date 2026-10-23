import os
from google.cloud import pubsub_v1


class PubSubClient:
    """Thin wrapper around Google Cloud Pub/Sub client."""

    def __init__(self):
        # Client picks up credentials from env variable GOOGLE_APPLICATION_CREDENTIALS
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish(self, topic_name: str, data: dict) -> str:
        """Publish a single JSON payload to a topic."""
        topic_path = self.publisher.topic_path(os.getenv("PROJECT_ID"), topic_name)
        # Pub/Sub expects bytes
        future = self.publisher.publish(
            topic_path, data=json.dumps(data).encode("utf-8")
        )
        # Block on result to get message ID
        message_id = future.result()
        return message_id

    def consume(self, subscription_name: str):
        """Consume a single message from a subscription (pull)."""
        subscription_path = self.subscriber.subscription_path(
            os.getenv("PROJECT_ID"), subscription_name
        )
        response = self.subscriber.pull(subscription_path, max_messages=1)
        if response.received_messages:
            msg = response.received_messages[0]
            data = msg.message.data.decode("utf-8")
            ack_id = msg.ack_id
            # Acknowledge after processing
            self.subscriber.acknowledge(subscription_path, [ack_id])
            return json.loads(data)
        return None

    def publish_batch(self, topic_name: str, messages: List[dict]) -> List[str]:
        """Publish multiple messages in a single batch."""
        topic_path = self.publisher.topic_path(os.getenv("PROJECT_ID"), topic_name)
        # Pub/Sub API requires a list of PubsubMessage objects
        pubsub_messages = [
            pubsub_v1.types.PubsubMessage(data=msg.encode()) for msg in messages
        ]
        # The publish method returns a list of futures; we wait on them
        futures = self.publisher.publish(topic_path, *pubsub_messages)
        message_ids = [f.result() for f in futures]
        return message_ids
