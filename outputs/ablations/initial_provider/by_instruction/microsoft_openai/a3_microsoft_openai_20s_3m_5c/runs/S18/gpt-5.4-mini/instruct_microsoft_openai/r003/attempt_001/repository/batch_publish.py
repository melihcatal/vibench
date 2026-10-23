import json

from azure.servicebus import ServiceBusMessage

from messaging_client import build_message_props, create_client, load_config
from messaging_models import normalize_batch


def publish_batch(items):
    config = load_config()
    messages = []
    for item in normalize_batch(items):
        messages.append(ServiceBusMessage(json.dumps(item), application_properties=build_message_props(item.get("id"), item.get("attributes"))))
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.batch_queue_name)
        with sender:
            sender.send_messages(messages)
    return {"queue": config.batch_queue_name, "count": len(messages)}
