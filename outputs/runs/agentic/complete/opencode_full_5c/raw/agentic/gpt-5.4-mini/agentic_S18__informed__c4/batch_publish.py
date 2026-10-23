from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config
from messaging_models import MessagePayload, payload_to_json


def batch_publish(events):
    config = load_config()
    messages = []
    for event in events:
        payload = MessagePayload(
            message_id=event["message_id"],
            content=event["content"],
            attributes=event.get("attributes", {}),
        )
        messages.append(
            ServiceBusMessage(
                payload_to_json(payload),
                message_id=payload.message_id,
                application_properties=payload.attributes,
            )
        )
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            sender.send_messages(messages)
    return {"published": len(messages)}
