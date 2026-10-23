import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import get_service_bus_client

def batch_publish(topic_name: str, events_data: list[dict]):
    """Publishes a batch of JSON events to an Azure Service Bus topic."""
    servicebus_client = get_service_bus_client()
    sender = servicebus_client.get_topic_sender(topic_name=topic_name)

    with sender:
        batch = sender.create_message_batch()
        for event_data in events_data:
            message_str = json.dumps(event_data)
            try:
                batch.add_message(ServiceBusMessage(message_str))
            except ValueError:
                # If the batch is full, send it and create a new one
                sender.send_messages(batch)
                print(f"Sent a batch of {len(batch)} messages.")
                batch = sender.create_message_batch()
                batch.add_message(ServiceBusMessage(message_str))
        
        if batch:
            sender.send_messages(batch)
            print(f"Published a final batch of {len(events_data)} events to topic '{topic_name}'.")

if __name__ == '__main__':
    # Example usage (replace with actual topic name and event data)
    topic = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")
    example_events = [
        {"id": "batch-001", "type": "order_created", "payload": {"order_id": "ORD-001"}},
        {"id": "batch-002", "type": "item_added", "payload": {"item_id": "ITEM-A"}},
        {"id": "batch-003", "type": "order_updated", "payload": {"order_id": "ORD-001", "status": "processing"}}
    ]
    batch_publish(topic, example_events)
