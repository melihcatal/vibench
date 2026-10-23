import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import load_messaging_config


def dead_letter(payload, config=None):
    cfg = load_messaging_config(config)
    with ServiceBusClient.from_connection_string(cfg["connection_string"]) as client:
        with client.get_queue_sender(queue_name=cfg["dead_letter_queue"]) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps(payload), content_type="application/json"))
    return {"destination": cfg["dead_letter_queue"], "sent": True}
