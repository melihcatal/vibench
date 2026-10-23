import json
from azure.servicebus import ServiceBusClient

from messaging_client import load_messaging_config
from messaging_models import normalize_received_message


def consume_event(config=None):
    cfg = load_messaging_config(config)
    with ServiceBusClient.from_connection_string(cfg["connection_string"]) as client:
        with client.get_subscription_receiver(topic_name=cfg["topic"], subscription_name=cfg["subscription"]) as receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=cfg["max_wait_time"])
            if not messages:
                return {"message": None}
            message = messages[0]
            payload = json.loads(str(message))
            normalized = normalize_received_message(message, payload)
            receiver.complete_message(message)
            return {"message": normalized}
