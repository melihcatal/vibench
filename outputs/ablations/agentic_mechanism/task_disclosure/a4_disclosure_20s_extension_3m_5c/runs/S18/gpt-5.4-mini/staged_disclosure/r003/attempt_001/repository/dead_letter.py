import os
import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


class DeadLetterPublisher:
    def __init__(self, project_id: Optional[str] = None, topic_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
        self.topic_id = topic_id or os.environ.get("DEAD_LETTER_TOPIC")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
        if not self.topic_id:
            raise ValueError("DEAD_LETTER_TOPIC is required")
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def send(self, message: Dict[str, Any], reason: str, original_topic: Optional[str] = None) -> str:
        payload = {
            "reason": reason,
            "original_topic": original_topic,
            "message": message,
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        future = self.publisher.publish(self.topic_path, data=data)
        return future.result()


def send_to_dead_letter(message: Dict[str, Any], reason: str, original_topic: Optional[str] = None) -> str:
    return DeadLetterPublisher().send(message=message, reason=reason, original_topic=original_topic)
