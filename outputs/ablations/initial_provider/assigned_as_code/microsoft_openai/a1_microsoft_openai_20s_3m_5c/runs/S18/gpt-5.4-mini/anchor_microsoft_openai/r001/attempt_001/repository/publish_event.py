import json
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def publish_event(payload, config=None):
    config = config or {}
    message_id = str(uuid.uuid4())
    with ServiceBusClient.from_connection_string(config['connection_string']) as client:
        with client.get_topic_sender(topic_name=config['topic']) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps(payload['event']),
                message_id=message_id, content_type='application/json'))
    return {'message_id': message_id}
