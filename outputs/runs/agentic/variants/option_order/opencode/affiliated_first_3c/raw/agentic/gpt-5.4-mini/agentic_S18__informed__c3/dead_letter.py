import json

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, get_queue_name


def dead_letter(message_body, reason: str = "processing_failed"):
    client = create_client()
    with client:
        sender = client.get_queue_sender(queue_name=get_queue_name())
        with sender:
            msg = ServiceBusMessage(
                json.dumps({"body": message_body, "reason": reason}),
                content_type="application/json",
            )
            msg.application_properties = {"dead_letter_reason": reason}
            sender.send_messages(msg)
    return {"provider": "azure-servicebus", "dead_lettered": True, "reason": reason}
