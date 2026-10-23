import json
from typing import Any, Dict, Optional

from messaging_client import get_sqs_client, require_config
from messaging_models import make_message_record


def consume_event(queue_url: Optional[str] = None, wait_time_seconds: int = 1) -> Dict[str, Any]:
    cfg = require_config()
    client = get_sqs_client()
    response = client.receive_message(
        QueueUrl=queue_url or cfg["queue_url"],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=["All"],
        AttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return make_message_record(provider="aws_sqs", action="consume", message_id=None, status="empty", details=response)
    message = messages[0]
    body = message.get("Body", "")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        payload = body
    return make_message_record(
        provider="aws_sqs",
        action="consume",
        message_id=message.get("MessageId") or message.get("ReceiptHandle"),
        status="received",
        payload=payload,
        details=message,
    )
