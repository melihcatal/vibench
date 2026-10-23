import os
import json
from typing import Any, Dict, Optional

import requests


SQS_API_VERSION = "2012-11-05"


class DeadLetterError(Exception):
    pass


def _sqs_endpoint(region: str) -> str:
    return f"https://sqs.{region}.amazonaws.com/"


def send_to_dead_letter(message: Dict[str, Any], *, queue_url: Optional[str] = None) -> Dict[str, Any]:
    region = os.getenv("AWS_REGION", "us-east-1")
    queue_url = queue_url or os.environ["AWS_SQS_DEAD_LETTER_QUEUE_URL"]
    body = json.dumps(message, separators=(",", ":"), sort_keys=True)

    response = requests.post(
        _sqs_endpoint(region),
        params={"Action": "SendMessage", "Version": SQS_API_VERSION},
        data={"QueueUrl": queue_url, "MessageBody": body},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    if response.status_code >= 400:
        raise DeadLetterError(f"Failed to send dead-letter message: {response.status_code} {response.text}")
    return {"queue_url": queue_url, "status_code": response.status_code, "message": body}


def dead_letter_failed_message(message: Dict[str, Any], error: str, *, queue_url: Optional[str] = None) -> Dict[str, Any]:
    payload = {
        "original_message": message,
        "error": error,
    }
    return send_to_dead_letter(payload, queue_url=queue_url)
