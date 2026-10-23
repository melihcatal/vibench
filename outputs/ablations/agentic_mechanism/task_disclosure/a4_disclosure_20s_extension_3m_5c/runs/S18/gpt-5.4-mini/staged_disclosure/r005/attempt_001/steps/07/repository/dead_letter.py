import os
from typing import Any, Dict, Optional

import boto3


class DeadLetterPublisher:
    def __init__(self, queue_url: Optional[str] = None, region_name: Optional[str] = None) -> None:
        self.queue_url = queue_url or os.environ.get("SQS_DEAD_LETTER_QUEUE_URL")
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        self.client = boto3.client("sqs", region_name=self.region_name)

    def send_failed_message(self, message: Dict[str, Any], error: Optional[str] = None) -> Dict[str, Any]:
        if not self.queue_url:
            raise ValueError("SQS_DEAD_LETTER_QUEUE_URL is required")
        body = {"message": message, "error": error}
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=str(body),
        )
        return response


def send_to_dead_letter(message: Dict[str, Any], error: Optional[str] = None) -> Dict[str, Any]:
    return DeadLetterPublisher().send_failed_message(message, error)
