import os

from azure.servicebus import ServiceBusMessage

from messaging_client import get_client, get_queue_name
from messaging_models import BatchMessageRequest, MessageResponse, to_json_bytes


def batch_publish(request: BatchMessageRequest) -> MessageResponse:
    queue_name = get_queue_name()
    with get_client() as client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            messages = []
            ids = []
            for item in request.messages:
                message_id = (
                    item.message_id or item.body.get("id") or os.urandom(8).hex()
                )
                ids.append(message_id)
                messages.append(
                    ServiceBusMessage(
                        to_json_bytes(item.body),
                        content_type=item.content_type,
                        message_id=message_id,
                    )
                )
            sender.send_messages(messages)
            return MessageResponse(
                message_id=ids[0] if ids else "",
                status="batch_sent",
                details={
                    "count": len(messages),
                    "queue": queue_name,
                    "message_ids": ids,
                },
            )
