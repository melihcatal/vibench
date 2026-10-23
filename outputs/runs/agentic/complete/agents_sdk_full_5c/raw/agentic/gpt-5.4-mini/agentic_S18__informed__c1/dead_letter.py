from azure.servicebus import ServiceBusMessage

from messaging_client import create_service_bus_client, get_dead_letter_queue_name
from messaging_models import normalize_message_body


def send_to_dead_letter(message_body, reason: str, error_description: str, original_message_id: str = ""):
    client = create_service_bus_client()
    queue_name = get_dead_letter_queue_name()
    payload = normalize_message_body(message_body)
    payload.update(
        {
            "dead_letter_reason": reason,
            "dead_letter_error_description": error_description,
            "original_message_id": original_message_id,
        }
    )
    with client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            message = ServiceBusMessage(str(payload), content_type="application/json")
            message.message_id = original_message_id or reason
            sender.send_messages(message)
    return {"status": "dead-lettered", "destination": queue_name}
