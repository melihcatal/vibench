from __future__ import annotations

from messaging_client import receive_one_message


def consume_event(queue_url: str, wait_time_seconds: int = 10) -> dict | None:
    message = receive_one_message(
        queue_url=queue_url, wait_time_seconds=wait_time_seconds
    )
    if message is None:
        return None
    return {
        "provider": "aws_sqs",
        "queue_url": queue_url,
        "message_id": message.message_id,
        "receipt_handle": message.receipt_handle,
        "body": message.body,
        "attributes": message.attributes,
    }
