import os
from google.cloud import pubsub_v1


class MessagingClient:
    def __init__(self, project_id=None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.publisher_client = pubsub_v1.PublisherClient()
        self.subscriber_client = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id):
        return self.publisher_client.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id):
        return self.subscriber_client.subscription_path(
            self.project_id, subscription_id
        )

    def get_dead_letter_topic_path(self, dead_letter_topic_id):
        return self.publisher_client.topic_path(self.project_id, dead_letter_topic_id)

    def publish_message(self, topic_path, data, attributes=None):
        future = self.publisher_client.publish(topic_path, data, **(attributes or {}))
        return future.result()

    def pull_messages(self, subscription_path, max_messages=1):
        response = self.subscriber_client.pull(
            subscription=subscription_path,
            max_messages=max_messages,
        )
        return response.received_messages

    def acknowledge_messages(self, subscription_path, ack_ids):
        self.subscriber_client.acknowledge(
            subscription=subscription_path,
            ack_ids=ack_ids,
        )

    def create_dead_letter_config(
        self, dead_letter_topic_path, max_delivery_attempts=5
    ):
        return pubsub_v1.types.DeadLetterPolicy(
            dead_letter_topic=dead_letter_topic_path,
            max_delivery_attempts=max_delivery_attempts,
        )
