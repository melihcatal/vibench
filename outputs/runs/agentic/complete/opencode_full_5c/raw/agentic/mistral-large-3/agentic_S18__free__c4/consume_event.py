import os
from google.cloud import pubsub_v1
from typing import Dict, Any, Optional
import json

# Provider-specific: Google Cloud Pub/Sub
# Model/Service: pubsub_v1.SubscriberClient
# Environment variable: GOOGLE_APPLICATION_CREDENTIALS


class EventConsumer:
    def __init__(self, project_id: str, subscription_id: str):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(
            project_id, subscription_id
        )

    def consume_event(self) -> Optional[Dict[str, Any]]:
        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            message.ack()
            self._last_message = {
                "data": json.loads(message.data.decode("utf-8")),
                "attributes": dict(message.attributes),
                "message_id": message.message_id,
            }

        self._last_message = None
        future = self.subscriber.subscribe(self.subscription_path, callback=callback)
        try:
            future.result(timeout=5.0)
        except Exception:
            future.cancel()
        return self._last_message
