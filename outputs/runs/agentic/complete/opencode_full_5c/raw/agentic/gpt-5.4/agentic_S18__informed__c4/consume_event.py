from __future__ import annotations

from messaging_client import receive_one_message


def consume_event(wait_time_seconds: int = 10) -> dict | None:
    message = receive_one_message(wait_time_seconds=wait_time_seconds)
    if message is None:
        return None
    return {
        "message_id": message.message_id,
        "receipt_handle": message.receipt_handle,
        "body": message.body,
        "attributes": message.attributes,
        "queue_url": message.queue_url,
    }
