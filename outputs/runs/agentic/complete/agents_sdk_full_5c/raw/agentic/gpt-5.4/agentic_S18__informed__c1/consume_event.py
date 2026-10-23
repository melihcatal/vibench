from __future__ import annotations

from typing import Optional

from messaging_client import get_sqs_client, get_sqs_queue_url
from messaging_models import ConsumedMessage, parse_sqs_body


PROVIDER = "aws-sqs"


def consume_event(queue_url: Optional[str] = None, wait_time_seconds: int = 10, visibility_timeout: int = 30) -> Optional[ConsumedMessage]:
    client = get_sqs_client()
    resolved_queue_url = get_sqs_queue_url(queue_url)
    response = client.receive_message(
        QueueUrl=resolved_queue_url,
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
    return ConsumedMessage(
        provider=PROVIDER,
        queue_url=resolved_queue_url,
        receipt_handle=message["ReceiptHandle"],
        body=parse_sqs_body(message["Body"]),
        message_id=message.get("MessageId", ""),
        attributes=message.get("MessageAttributes", {}),
    )
