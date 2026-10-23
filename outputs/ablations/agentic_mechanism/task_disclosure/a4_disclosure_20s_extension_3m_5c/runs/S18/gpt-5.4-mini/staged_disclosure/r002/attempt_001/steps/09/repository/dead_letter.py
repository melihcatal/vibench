import json
import os
from typing import Any, Dict, Optional

import requests


class DeadLetterPublisher:
    def __init__(self, queue_url: Optional[str] = None, region: Optional[str] = None):
        self.queue_url = queue_url or os.environ.get("AWS_SQS_DEAD_LETTER_QUEUE_URL")
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        if not self.queue_url:
            raise ValueError("AWS_SQS_DEAD_LETTER_QUEUE_URL is required")

    def send_failed_message(self, message: Any, reason: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "failed_message": message,
            "reason": reason,
            "metadata": metadata or {},
        }
        body = json.dumps(payload, default=str)
        response = requests.post(
            self.queue_url,
            headers={
                "Content-Type": "application/json",
                "X-AWS-Region": self.region,
            },
            data=body,
            timeout=30,
        )
        response.raise_for_status()
        return {"status_code": response.status_code, "response_text": response.text}


def send_to_dead_letter(message: Any, reason: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return DeadLetterPublisher().send_failed_message(message, reason, metadata)
