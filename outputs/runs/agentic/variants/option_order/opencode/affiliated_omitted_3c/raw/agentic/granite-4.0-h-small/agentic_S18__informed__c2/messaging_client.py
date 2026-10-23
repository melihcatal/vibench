import os
from alibabacloud_mns import MnsClient


class PubSubClient:
    """Thin wrapper around Alibaba Cloud MNS (RocketMQ) SDK for unified Pub/Sub operations.

    Uses environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET for authentication.
    """

    def __init__(self):
        endpoint = os.getenv(
            "ALIBABA_CLOUD_MNS_ENDPOINT", "https://mns.cn-hangzhou.aliyuncs.com"
        )
        access_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
        secret_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        self.client = MnsClient(endpoint, access_key, secret_key)

    def publish(self, topic_name: str, message: str):
        """Publish a single message to a topic."""
        topic = self.client.get_topic_ref(topic_name)
        return topic.publish_message(message)

    def consume(self, subscription_name: str):
        """Consume the next available message from a subscription."""
        subscription = self.client.get_subscription_ref(subscription_name)
        return subscription.consume_message()

    def acknowledge(self, subscription_name: str, receipt_handle: str):
        """Acknowledge a consumed message."""
        subscription = self.client.get_subscription_ref(subscription_name)
        return subscription.ack_message(receipt_handle)

    def batch_publish(self, topic_name: str, messages: list[str], batch_id: str):
        """Publish multiple messages as a batch."""
        topic = self.client.get_topic_ref(topic_name)
        return topic.batch_publish_message(messages, batch_id=batch_id)

    def fetch_failed_message(self, subscription_name: str, message_id: str):
        """Placeholder to retrieve a failed message for dead-lettering."""
        # Alibaba MNS does not expose failed messages directly; this would require DLQ processing logic.
        return None
