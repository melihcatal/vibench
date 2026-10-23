import os
from google.cloud import pubsub_v1
from typing import List, Dict, Any
import json

# Provider: Google Cloud Pub/Sub
# Model/Service: pubsub_v1.PublisherClient
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class BatchEventPublisher:
    def __init__(self, project_id: str, topic_id: str):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish_batch(self, messages: List[Dict[str, Any]]) -> List[str]:
        """
        Publishes a batch of messages to Google Cloud Pub/Sub topic.
        Returns a list of message IDs.
        """
        futures = []
        for message in messages:
            data = json.dumps(message).encode("utf-8")
            future = self.publisher.publish(self.topic_path, data)
            futures.append(future)

        return [future.result() for future in futures]
