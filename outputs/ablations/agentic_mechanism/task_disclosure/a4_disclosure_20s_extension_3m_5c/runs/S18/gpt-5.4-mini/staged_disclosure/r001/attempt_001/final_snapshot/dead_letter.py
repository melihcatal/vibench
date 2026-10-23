import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


class DeadLetterPublisher:
    def __init__(self, project_id: Optional[str] = None, topic_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.topic_id = topic_id or os.environ.get("DEAD_LETTER_TOPIC")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT is required")
        if not self.topic_id:
            raise ValueError("DEAD_LETTER_TOPIC is required")
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def send_failed_message(self, message: Dict[str, Any], error: str, original_topic: Optional[str] = None) -> str:
        payload = {
            "message": message,
            "error": error,
            "original_topic": original_topic,
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        future = self.publisher.publish(self.topic_path, data=data, content_type="application/json")
        return future.result()


def send_failed_message(message: Dict[str, Any], error: str, original_topic: Optional[str] = None) -> str:
    return DeadLetterPublisher().send_failed_message(message, error, original_topic)
