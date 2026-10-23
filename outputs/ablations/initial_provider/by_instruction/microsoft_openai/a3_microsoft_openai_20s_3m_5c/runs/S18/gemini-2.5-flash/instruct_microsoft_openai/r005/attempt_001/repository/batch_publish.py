import os
import uuid
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from messaging_client import get_servicebus_client, get_topic_name
from messaging_models import PubSubEvent

def publish_batch_events(event_data_list: list[dict]):
    client = get_servicebus_client()
    topic_name = get_topic_name()

    sender = client.get_topic_sender(topic_name=topic_name)
    with sender:
        batch = sender.create_message_batch()
        for event_data in event_data_list:
            event = PubSubEvent(
                id=str(uuid.uuid4()),
                source="/my-application/events",
                type="com.example.batch.event.v1",
                specversion="1.0",
                time=datetime.utcnow().isoformat() + "Z",
                data=event_data
            )
            try:
                batch.add_message(ServiceBusMessage(event.to_json()))
                print(f"Added event {event.id} to batch.")
            except ValueError:
                # Batch is full, send it and create a new one
                sender.send_messages(batch)
                print("Batch sent. Creating a new batch.")
                batch = sender.create_message_batch()
                batch.add_message(ServiceBusMessage(event.to_json()))
                print(f"Added event {event.id} to new batch.")
        
        if len(batch) > 0:
            sender.send_messages(batch)
            print("Final batch sent.")

    client.close()
    print(f"Published a batch of {len(event_data_list)} events to topic: {topic_name}")

if __name__ == "__main__":
    # Example usage: Ensure AZURE_SERVICEBUS_CONNECTION_STRING and AZURE_SERVICEBUS_TOPIC_NAME are set.
    example_events_data = [
        {"eventType": "ProductViewed", "productId": "prod1", "userId": "userA"},
        {"eventType": "ProductViewed", "productId": "prod2", "userId": "userB"},
        {"eventType": "ProductAddedToCart", "productId": "prod1", "userId": "userA", "quantity": 1}
    ]
    publish_batch_events(example_events_data)
