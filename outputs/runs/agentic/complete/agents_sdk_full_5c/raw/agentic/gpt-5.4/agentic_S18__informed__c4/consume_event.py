from __future__ import annotations

import json
from typing import Optional

from messaging_client import get_sqs_client, resolve_queue_url
from messaging_models import ConsumedMessage


PROVIDER = "amazon_sqs"


def consume_event(queue_url: Optional[str] = None, wait_time_seconds: int = 10, visibility_timeout: int = 30) -> Optional[ConsumedMessage]:
    client = get_sqs_client()
    source = resolve_queue_url(queue_url)
    response = client.receive_message(
        QueueUrl=source,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time_seconds,
        VisibilityTimeout=visibility_timeout,
        MessageAttributeNames=["All"],
        AttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    attributes = {
        key: value.get("StringValue")
        for key, value in message.get("MessageAttributes", {}).items()
    }
    return ConsumedMessage(
        message_id=message["MessageId"],
        body=json.loads(message["Body"]),
        attributes=attributes,
        delivery_count=int(message.get("Attributes", {}).get("ApproximateReceiveCount", "1")),
        raw_receipt_handle=message.get("ReceiptHandle"),
    )
