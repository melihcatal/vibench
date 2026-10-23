import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import get_config, require
from messaging_models import normalize_payload


def dead_letter_message(message, reason="processing_failed"):
    config = get_config()
    client = ServiceBusClient.from_connection_string(require(config["azure_connection_string"], "AZURE_SERVICE_BUS_CONNECTION_STRING"))
    dead_letter_queue = require(config["azure_dead_letter_queue"], "AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE")
    payload = normalize_payload(message)
    with client:
        sender = client.get_queue_sender(dead_letter_queue)
        with sender:
            sender.send_messages(ServiceBusMessage(json.dumps({"reason": reason, "message": payload}, ensure_ascii=False)))
    return {"provider": "azure.servicebus", "dead_letter_queue": dead_letter_queue, "reason": reason}
