import json

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config


def send_dead_letter(payload, reason="processing_failed"):
    config = load_config()
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.dead_letter_queue_name)
        with sender:
            sender.send_messages(ServiceBusMessage(json.dumps(payload), application_properties={"dead_letter_reason": reason}))
    return {"destination": config.dead_letter_queue_name, "status": "sent"}
