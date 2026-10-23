import os
import json
from typing import Any, Dict, Optional

import boto3


class DeadLetterSender:
    def __init__(self, queue_url: Optional[str] = None, region_name: Optional[str] = None):
        self.queue_url = queue_url or os.environ["AWS_SQS_DEAD_LETTER_QUEUE_URL"]
        self.sqs = boto3.client("sqs", region_name=region_name or os.getenv("AWS_REGION"))

    def send_failed_message(self, message: Dict[str, Any], reason: str) -> Dict[str, Any]:
        payload = {
            "message": message,
            "reason": reason,
        }
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(payload),
        )
        return {
            "message_id": response.get("MessageId"),
            "md5_of_message_body": response.get("MD5OfMessageBody"),
        }


def send_to_dead_letter(message: Dict[str, Any], reason: str, queue_url: Optional[str] = None) -> Dict[str, Any]:
    return DeadLetterSender(queue_url=queue_url).send_failed_message(message, reason)
