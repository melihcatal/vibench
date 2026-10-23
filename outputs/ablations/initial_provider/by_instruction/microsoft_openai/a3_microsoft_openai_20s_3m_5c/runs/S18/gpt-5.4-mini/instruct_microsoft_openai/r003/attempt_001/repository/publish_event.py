import json
import os

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config
from messaging_models import normalize_payload


def publish_event(payload):
    config = load_config()
    message = normalize_payload(payload)
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            sender.send_messages(ServiceBusMessage(json.dumps(message), message_id=message.get("id") or os.getenv("MESSAGE_ID")))
    return {"queue": config.queue_name, "status": "published"}
