import os
import json
from azure.servicebus import ServiceBusMessage
from messaging_client import get_servicebus_client
from messaging_models import EventMessage


def publish_event(event: EventMessage, queue_name: str):
    client = get_servicebus_client()
    sender = client.get_queue_sender(queue_name=queue_name)
    with sender:
        message_body = event.to_json_string()
        servicebus_message = ServiceBusMessage(message_body)
        sender.send_messages(servicebus_message)
    client.close()


if __name__ == "__main__":
    # Example usage
    queue_name = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "myqueue")
    event = EventMessage(
        message_id="123",
        payload={"type": "order_created", "order_id": "ORD-001", "amount": 100.50},
        attributes={"source": "web_app", "timestamp": "2026-04-20T10:00:00Z"},
    )
    print(f"Publishing event to {queue_name}...")
    publish_event(event, queue_name)
    print("Event published.")
