import os
from google.cloud import pubsub_v1
from typing import Dict, Any, Optional
import json

# Provider: Google Cloud Pub/Sub
# Model/Service: pubsub_v1.SubscriberClient
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class EventConsumer:
    def __init__(self, project_id: str, subscription_id: str):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(
            project_id, subscription_id
        )

    def consume_event(self) -> Optional[Dict[str, Any]]:
        """
        Consumes one message from Google Cloud Pub/Sub subscription.
        Returns None if no message is available.
        """
        response = self.subscriber.pull(
            request={
                "subscription": self.subscription_path,
                "max_messages": 1,
                "return_immediately": True,
            }
        )

        if not response.received_messages:
            return None

        message = response.received_messages[0]
        data = json.loads(message.message.data.decode("utf-8"))
        self.subscriber.acknowledge(
            request={
                "subscription": self.subscription_path,
                "ack_ids": [message.ack_id],
            }
        )
        return data
