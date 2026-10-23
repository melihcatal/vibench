import json
import uuid
from azure.servicebus import ServiceBusMessage

from messaging_client import create_service_bus_client, get_topic_name
from messaging_models import EventRequest, PublishResult


def publish_event(payload: dict, event_type: str = "customer.event") -> PublishResult:
    event = EventRequest(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        payload=payload,
        attributes={"source": "publish_event.py"},
    )
    client = create_service_bus_client()
    topic_name = get_topic_name()
    with client:
        sender = client.get_topic_sender(topic_name=topic_name)
        with sender:
            message = ServiceBusMessage(event.to_json(), content_type="application/json")
            message.subject = event.event_type
            message.message_id = event.event_id
            sender.send_messages(message)
    return PublishResult(message_id=event.event_id, status="sent", destination=topic_name)


if __name__ == "__main__":
    publish_event({"example": True})
