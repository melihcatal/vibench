import os
from google.cloud import pubsub_v1
from typing import Dict, Any
import json

# Provider: Google Cloud Pub/Sub
# Model/Service: pubsub_v1.PublisherClient
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class DeadLetterSender:
    def __init__(self, project_id: str, dead_letter_topic_id: str):
        self.project_id = project_id
        self.dead_letter_topic_id = dead_letter_topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.dead_letter_topic_path = self.publisher.topic_path(
            project_id, dead_letter_topic_id
        )

    def send_to_dead_letter(
        self, message_data: Dict[str, Any], error_details: str
    ) -> str:
        """
        Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.
        """
        message_data["_error_details"] = error_details
        data = json.dumps(message_data).encode("utf-8")
        future = self.publisher.publish(self.dead_letter_topic_path, data)
        return future.result()
