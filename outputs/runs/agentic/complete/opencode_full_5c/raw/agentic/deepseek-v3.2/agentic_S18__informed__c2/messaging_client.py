import os
import json
from typing import Optional, Dict, Any
from google.cloud import pubsub_v1


class PubSubClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.publisher_client = pubsub_v1.PublisherClient()
        self.subscriber_client = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        return self.publisher_client.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        return self.subscriber_client.subscription_path(
            self.project_id, subscription_id
        )

    def format_message(
        self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None
    ) -> bytes:
        message_data = json.dumps(data).encode("utf-8")
        return message_data

    def parse_message(self, message: pubsub_v1.types.PubsubMessage) -> Dict[str, Any]:
        data = json.loads(message.data.decode("utf-8"))
        return {
            "data": data,
            "attributes": dict(message.attributes),
            "message_id": message.message_id,
            "publish_time": message.publish_time,
        }

    def create_dead_letter_topic_name(self, original_topic: str) -> str:
        return f"{original_topic}-dead-letter"
