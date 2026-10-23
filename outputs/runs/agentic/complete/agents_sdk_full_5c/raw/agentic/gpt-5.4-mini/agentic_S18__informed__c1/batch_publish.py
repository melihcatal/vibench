import uuid
from typing import Iterable, List

from azure.servicebus import ServiceBusMessage

from messaging_client import create_service_bus_client, get_topic_name
from messaging_models import BatchItem, PublishResult


def batch_publish(items: Iterable[BatchItem]) -> List[PublishResult]:
    client = create_service_bus_client()
    topic_name = get_topic_name()
    results: List[PublishResult] = []
    with client:
        sender = client.get_topic_sender(topic_name=topic_name)
        with sender:
            messages = []
            for item in items:
                msg = ServiceBusMessage(item.to_payload(), content_type="application/json")
                msg.message_id = item.message_id or str(uuid.uuid4())
                for key, value in (item.application_properties or {}).items():
                    msg.application_properties[key] = value
                messages.append(msg)
                results.append(PublishResult(message_id=msg.message_id, status="queued", destination=topic_name))
            sender.send_messages(messages)
    return results
