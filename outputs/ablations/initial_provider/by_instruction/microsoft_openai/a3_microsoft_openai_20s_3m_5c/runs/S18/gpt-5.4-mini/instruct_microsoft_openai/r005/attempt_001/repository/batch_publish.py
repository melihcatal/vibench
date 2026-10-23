import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import get_config, require
from messaging_models import make_batch


def batch_publish(messages):
    config = get_config()
    client = ServiceBusClient.from_connection_string(require(config["azure_connection_string"], "AZURE_SERVICE_BUS_CONNECTION_STRING"))
    queue_name = require(config["azure_queue_name"], "AZURE_SERVICE_BUS_QUEUE_NAME")
    batch = make_batch(messages)
    with client:
        sender = client.get_queue_sender(queue_name)
        with sender:
            for record in batch:
                sender.send_messages(ServiceBusMessage(json.dumps(record.payload, ensure_ascii=False), message_id=record.message_id, application_properties=record.attributes))
    return {"provider": "azure.servicebus", "count": len(batch), "queue": queue_name}
