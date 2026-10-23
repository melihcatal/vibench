import json
import os
from typing import Any, Dict, Optional

import requests


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_API_VERSION = "2012-11-05"


def _dead_letter_queue_url() -> str:
    url = os.getenv("AWS_SQS_DEAD_LETTER_QUEUE_URL")
    if not url:
        raise ValueError("AWS_SQS_DEAD_LETTER_QUEUE_URL is required")
    return url


def _request_params(queue_url: str, body: str, message_group_id: Optional[str], message_deduplication_id: Optional[str]) -> Dict[str, str]:
    params: Dict[str, str] = {
        "Action": "SendMessage",
        "Version": SQS_API_VERSION,
        "MessageBody": body,
        "QueueUrl": queue_url,
    }
    if message_group_id:
        params["MessageGroupId"] = message_group_id
    if message_deduplication_id:
        params["MessageDeduplicationId"] = message_deduplication_id
    return params


def send_to_dead_letter(
    failed_message: Dict[str, Any],
    error_reason: str,
    *,
    message_group_id: Optional[str] = None,
    message_deduplication_id: Optional[str] = None,
) -> Dict[str, Any]:
    queue_url = _dead_letter_queue_url()
    payload = {
        "provider": "aws_sqs",
        "region": AWS_REGION,
        "error_reason": error_reason,
        "failed_message": failed_message,
    }
    response = requests.post(
        "https://sqs.amazonaws.com/",
        data=_request_params(
            queue_url,
            json.dumps(payload, separators=(",", ":"), ensure_ascii=False),
            message_group_id,
            message_deduplication_id,
        ),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    return {"queued": True, "status_code": response.status_code, "queue_url": queue_url}
