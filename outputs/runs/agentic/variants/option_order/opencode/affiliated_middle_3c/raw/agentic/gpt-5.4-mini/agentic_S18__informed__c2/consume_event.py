from azure.servicebus import ServiceBusReceiveMode

from messaging_client import get_client, get_queue_name
from messaging_models import MessageResponse


def consume_event() -> MessageResponse:
    queue_name = get_queue_name()
    with get_client() as client:
        receiver = client.get_queue_receiver(
            queue_name=queue_name, receive_mode=ServiceBusReceiveMode.PEEK_LOCK
        )
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return MessageResponse(
                    message_id="", status="empty", details={"queue": queue_name}
                )
            message = messages[0]
            receiver.complete_message(message)
            return MessageResponse(
                message_id=str(message.message_id or ""),
                status="consumed",
                details={"body": str(message), "queue": queue_name},
            )
