import os
from typing import List
from azure.servicebus import ServiceBusMessage
from messaging_client import get_servicebus_client
from messaging_models import EventMessage


def batch_publish_events(events: List[EventMessage], queue_name: str):
    client = get_servicebus_client()
    sender = client.get_queue_sender(queue_name=queue_name)
    with sender:
        batch = sender.create_message_batch()
        for event in events:
            message_body = event.to_json_string()
            servicebus_message = ServiceBusMessage(message_body)
            try:
                batch.add_message(servicebus_message)
            except ValueError:
                # Batch is full, send it and create a new one
                sender.send_messages(batch)
                batch = sender.create_message_batch()
                batch.add_message(servicebus_message)
        if batch:
            sender.send_messages(batch)
    client.close()


if __name__ == "__main__":
    # Example usage
    queue_name = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "myqueue")
    events_to_publish = [
        EventMessage(
            "456", {"type": "product_updated", "product_id": "PROD-001", "price": 29.99}
        ),
        EventMessage(
            "789",
            {
                "type": "user_registered",
                "user_id": "USER-001",
                "email": "test@example.com",
            },
        ),
        EventMessage(
            "101",
            {
                "type": "order_shipped",
                "order_id": "ORD-001",
                "tracking_code": "TRACK-123",
            },
        ),
    ]
    print(f"Publishing batch of {len(events_to_publish)} events to {queue_name}...")
    batch_publish_events(events_to_publish, queue_name)
    print("Batch events published.")
