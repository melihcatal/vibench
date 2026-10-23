import os
from google.cloud import pubsub_v1
from google.oauth2 import service_account

class PubSubClient:
    """Helper wrapper for Google Cloud Pub/Sub operations."""
    def __init__(self):
        # Use credentials specified in environment
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        )
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

    def publish(self, topic: str, message: dict):
        """Publish a single message to a topic."""
        future = self.publisher.publish(topic=topic, data=message['data'], **message.get('attributes', {}))
        msg_id = future.result()
        return {'message_id': msg_id}

    def publish_batch(self, topic: str, messages: list[dict]):
        """Publish a list of messages as a batch."""
        future = self.publisher.publish(topic=topic, messages=messages)
        future.result()

    def pull(self, subscription: str, max_messages: int = 1):
        """Pull messages from a subscription, synchronously."""
        response = self.subscriber.pull(subscription=subscription, max_messages=max_messages, return_immediately=True)
        return response.received_messages or []

    def acknowledge(self, subscription: str, message_ids: list[str]):
        """Acknowledge pulled messages."""
        self.subscriber.acknowledge(subscription=subscription, message_ids=message_ids)
