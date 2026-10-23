from __future__ import annotations

import json

from messaging_client import get_queue_name, get_servicebus_client
from messaging_models import ConsumedMessage, normalize_json_payload


def consume_one_message(
    max_wait_time: int = 10, auto_complete: bool = True
) -> ConsumedMessage | None:
    queue_name = get_queue_name()
    with get_servicebus_client() as client:
        with client.get_queue_receiver(
            queue_name=queue_name, max_wait_time=max_wait_time
        ) as receiver:
            messages = receiver.receive_messages(
                max_message_count=1, max_wait_time=max_wait_time
            )
            if not messages:
                return None
            message = messages[0]
            body_text = b"".join(
                bytes(part) if not isinstance(part, bytes) else part
                for part in message.body
            ).decode("utf-8")
            consumed = ConsumedMessage(
                message_id=message.message_id or "",
                ack_token=message.lock_token,
                body=normalize_json_payload(body_text),
                attributes={
                    str(k): str(v)
                    for k, v in (message.application_properties or {}).items()
                },
                delivery_count=message.delivery_count,
                published_at=message.enqueued_time_utc.isoformat()
                if message.enqueued_time_utc
                else None,
            )
            if auto_complete:
                receiver.complete_message(message)
            return consumed


def consume_one_message_json(
    max_wait_time: int = 10, auto_complete: bool = True
) -> str | None:
    message = consume_one_message(
        max_wait_time=max_wait_time, auto_complete=auto_complete
    )
    if message is None:
        return None
    return json.dumps(message.body, ensure_ascii=False)
