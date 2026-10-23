import json
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import get_servicebus_client

def batch_publish(payloads, config=None):
    config = config or {}
    message_ids = []
    client = get_servicebus_client(config['connection_string'])
    with client.get_topic_sender(topic_name=config['topic']) as sender:
        for payload in payloads:
            message_id = str(uuid.uuid4())
            sender.send_messages(ServiceBusMessage(json.dumps(payload),
                message_id=message_id, content_type='application/json'))
            message_ids.append(message_id)
    return {'message_ids': message_ids}