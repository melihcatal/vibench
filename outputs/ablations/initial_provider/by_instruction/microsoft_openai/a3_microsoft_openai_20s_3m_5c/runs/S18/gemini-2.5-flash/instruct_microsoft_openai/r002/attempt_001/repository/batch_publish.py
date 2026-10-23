from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import json

def batch_publish_events(topic_name: str, events: list[dict]):
    """
    Publishes a batch of JSON events to an Azure Service Bus topic.
    """
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_topic_sender(topic_name=topic_name)
        with sender:
            batch = sender.create_message_batch()
            for event_data in events:
                message = ServiceBusMessage(json.dumps(event_data))
                try:
                    batch.add_message(message)
                except ValueError:
                    # Batch is full, send the current batch and create a new one
                    sender.send_messages(batch)
                    print(f"Sent a batch of {len(batch)} messages.")
                    batch = sender.create_message_batch()
                    batch.add_message(message)
            if batch:
                sender.send_messages(batch)
                print(f"Sent final batch of {len(batch)} messages.")

if __name__ == "__main__":
    # Example usage
    sample_events = [
        {"id": "1", "type": "OrderCreated", "data": {"item": "Laptop", "quantity": 1}},
        {"id": "2", "type": "UserRegistered", "data": {"username": "testuser"}},
        {"id": "3", "type": "ProductViewed", "data": {"product_id": "XYZ"}},
    ]
    topic = os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME", "my_topic")
    batch_publish_events(topic, sample_events)
