import os

from azure.servicebus import ServiceBusMessage

from messaging_client import get_client, get_queue_name
from messaging_models import MessageRequest, MessageResponse, to_json_bytes


def publish_event(request: MessageRequest) -> MessageResponse:
    queue_name = get_queue_name()
    with get_client() as client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            message = ServiceBusMessage(
                to_json_bytes(request.body),
                content_type=request.content_type,
                message_id=request.message_id
                or request.body.get("id")
                or os.urandom(8).hex(),
            )
            sender.send_messages(message)
            return MessageResponse(
                message_id=message.message_id,
                status="sent",
                details={"queue": queue_name},
            )
