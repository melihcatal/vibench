from __future__ import annotations

from typing import Optional

from messaging_client import get_queue_url, sqs_client
from messaging_models import ConsumedMessage, decode_message_body


def consume_event(
    queue_url: str | None = None, wait_time_seconds: int = 5
) -> Optional[ConsumedMessage]:
    client = sqs_client()
    source_queue = queue_url or get_queue_url("AWS_SQS_QUEUE_URL")
    response = client.receive_message(
        QueueUrl=source_queue,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    attributes = {
        key: value.get("StringValue", "")
        for key, value in message.get("MessageAttributes", {}).items()
    }
    return ConsumedMessage(
        message_id=message["MessageId"],
        body=decode_message_body(message["Body"]),
        attributes=attributes,
        receipt_handle=message["ReceiptHandle"],
        queue_url=source_queue,
    )
