import uuid
from azure.servicebus import ServiceBusMessage
from messaging_client import open_client, topic_name
from messaging_models import build_message_body, message_attributes


def batch_publish(messages, config=None):
    config = config or {}
    ids = []
    with open_client(config) as client:
        with client.get_topic_sender(topic_name(config)) as sender:
            batch = []
            for payload in messages:
                message_id = str(uuid.uuid4())
                ids.append(message_id)
                batch.append(ServiceBusMessage(build_message_body(payload), message_id=message_id, application_properties=message_attributes(payload), content_type='application/json'))
            sender.send_messages(batch)
    return {'message_ids': ids}
