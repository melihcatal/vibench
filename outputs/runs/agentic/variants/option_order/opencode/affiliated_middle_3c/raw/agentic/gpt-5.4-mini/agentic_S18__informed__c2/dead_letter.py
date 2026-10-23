from messaging_client import get_client, get_dead_letter_queue_name
from messaging_models import MessageRequest, MessageResponse, to_json_bytes


def dead_letter_message(request: MessageRequest) -> MessageResponse:
    queue_name = get_dead_letter_queue_name()
    with get_client() as client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            sender.send_messages(to_json_bytes(request.body))
            return MessageResponse(
                message_id=request.message_id or "",
                status="dead-lettered",
                details={"queue": queue_name},
            )
