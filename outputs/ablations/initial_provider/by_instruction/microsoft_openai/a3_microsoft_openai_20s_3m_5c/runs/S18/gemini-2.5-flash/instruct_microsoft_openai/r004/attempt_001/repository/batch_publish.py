import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_models import Event
from typing import List

def batch_publish_events(events: List[Event]):
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    queue_name = os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME", "myqueue")

    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        with client.get_queue_sender(queue_name) as sender:
            message_batch = sender.create_message_batch()
            for event in events:
                message_body = json.dumps(event.dict())
                try:
                    message_batch.add_message(ServiceBusMessage(message_body))
                except ValueError:
                    # Batch is full, send the current batch and create a new one
                    sender.send_messages(message_batch)
                    print(f"Sent a batch of {len(message_batch)} messages.")
                    message_batch = sender.create_message_batch()
                    message_batch.add_message(ServiceBusMessage(message_body))
            if message_batch:
                sender.send_messages(message_batch)
                print(f"Sent a batch of {len(message_batch)} messages.")

if __name__ == "__main__":
    example_events = [
        Event(id="1", type="order_created", data={"item": "Laptop", "quantity": 1}),
        Event(id="2", type="order_updated", data={"item": "Mouse", "quantity": 2}),
        Event(id="3", type="user_deleted", data={"user_id": "abc"})
    ]
    batch_publish_events(example_events)
