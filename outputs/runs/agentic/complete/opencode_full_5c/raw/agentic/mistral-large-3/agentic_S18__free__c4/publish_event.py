import os
from google.cloud import pubsub_v1
from typing import Dict, Any
import json

# Provider-specific: Google Cloud Pub/Sub
# Model/Service: pubsub_v1.PublisherClient
# Environment variable: GOOGLE_APPLICATION_CREDENTIALS


class EventPublisher:
    def __init__(self, project_id: str, topic_id: str):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish_event(
        self, event_data: Dict[str, Any], attributes: Dict[str, str] = None
    ) -> str:
        data = json.dumps(event_data).encode("utf-8")
        future = self.publisher.publish(self.topic_path, data, **(attributes or {}))
        return future.result()
