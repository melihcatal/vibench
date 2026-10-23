import json

from azure.servicebus import ServiceBusMessage

from messaging_client import create_servicebus_client, load_config


def dead_letter_message(payload: dict, reason: str) -> dict:
    config = load_config()
    dead_letter_name = config.dead_letter_queue_name or config.queue_name
    message = ServiceBusMessage(json.dumps({"payload": payload, "reason": reason}), content_type="application/json")
    with create_servicebus_client() as client:
        sender = client.get_queue_sender(queue_name=dead_letter_name)
        with sender:
            sender.send_messages(message)
    return {"sent": True, "destination": dead_letter_name}


if __name__ == "__main__":
    print(json.dumps(dead_letter_message({"id": "failed"}, "processing_error")))
