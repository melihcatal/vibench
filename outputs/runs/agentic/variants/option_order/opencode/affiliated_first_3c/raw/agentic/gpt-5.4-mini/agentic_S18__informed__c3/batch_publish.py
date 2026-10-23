import json

from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, get_topic_name
from messaging_models import parse_batch_items, dataclass_to_dict


def batch_publish(items):
    parsed = parse_batch_items(items)
    client = create_client()
    with client:
        sender = client.get_topic_sender(topic_name=get_topic_name())
        with sender:
            messages = []
            for item in parsed:
                msg = ServiceBusMessage(
                    json.dumps(item.body, ensure_ascii=False),
                    content_type="application/json",
                    message_id=item.message_id,
                )
                msg.application_properties = item.attributes or {}
                messages.append(msg)
            sender.send_messages(messages)
    return [dataclass_to_dict(item) for item in parsed]
