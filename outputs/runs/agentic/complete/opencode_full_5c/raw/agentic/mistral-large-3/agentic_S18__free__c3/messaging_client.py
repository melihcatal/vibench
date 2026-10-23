import os
from google.cloud import pubsub_v1
from typing import Optional, Dict, Any
import json

# Provider: Google Cloud Pub/Sub
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class MessagingClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    def get_publisher_client(self) -> pubsub_v1.PublisherClient:
        """Returns a configured Google Cloud Pub/Sub PublisherClient."""
        return pubsub_v1.PublisherClient()

    def get_subscriber_client(self) -> pubsub_v1.SubscriberClient:
        """Returns a configured Google Cloud Pub/Sub SubscriberClient."""
        return pubsub_v1.SubscriberClient()

    def normalize_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes message payload for consistent processing."""
        normalized = {
            "id": message.get("id", ""),
            "timestamp": message.get("timestamp", ""),
            "payload": message.get("payload", {}),
            "attributes": message.get("attributes", {}),
        }
        return normalized
