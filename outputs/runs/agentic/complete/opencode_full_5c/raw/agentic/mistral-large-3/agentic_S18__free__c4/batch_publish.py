import os
from google.cloud import pubsub_v1
from typing import List, Dict, Any
import json

# Provider-specific: Google Cloud Pub/Sub
# Model/Service: pubsub_v1.PublisherClient
# Environment variable: GOOGLE_APPLICATION_CREDENTIALS


class BatchEventPublisher:
    def __init__(self, project_id: str, topic_id: str):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish_batch(self, messages: List[Dict[str, Any]]) -> List[str]:
        futures = []
        for message in messages:
            data = json.dumps(message["data"]).encode("utf-8")
            attributes = message.get("attributes", {})
            future = self.publisher.publish(self.topic_path, data, **attributes)
            futures.append(future)

        return [future.result() for future in futures]
