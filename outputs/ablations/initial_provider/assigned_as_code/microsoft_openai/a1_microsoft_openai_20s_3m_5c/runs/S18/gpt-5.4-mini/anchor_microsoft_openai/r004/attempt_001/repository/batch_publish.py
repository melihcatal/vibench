import json
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import load_messaging_config


def batch_publish(events, config=None):
    cfg = load_messaging_config(config)
    message_ids = []
    with ServiceBusClient.from_connection_string(cfg["connection_string"]) as client:
        with client.get_topic_sender(topic_name=cfg["topic"]) as sender:
            messages = []
            for index, event in enumerate(events):
                message_id = str(uuid.uuid4())
                message_ids.append(message_id)
                messages.append(ServiceBusMessage(json.dumps(event), message_id=message_id, application_properties={"batch_index": index}, content_type="application/json"))
            sender.send_messages(messages)
    return {"message_ids": message_ids, "count": len(message_ids)}
