import json

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config
from messaging_models import encode_json_bytes


def send_to_dead_letter(payload: dict, reason: str, source_message_id: str) -> str:
    config = load_config()
    body = {
        "reason": reason,
        "source_message_id": source_message_id,
        "payload": payload,
    }
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.dead_letter_queue)
        message = ServiceBusMessage(
            body=encode_json_bytes(body),
            content_type="application/json",
            message_id=source_message_id,
            application_properties={
                "reason": reason,
                "source_message_id": source_message_id,
            },
        )
        with sender:
            sender.send_messages(message)
    return source_message_id


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "message_id": send_to_dead_letter(
                    {"error": True}, "processing_failed", "abc-123"
                )
            }
        )
    )
