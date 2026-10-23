import os
import uuid
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from messaging_client import get_servicebus_client, get_topic_name
from messaging_models import PubSubEvent

def publish_event(event_data: dict):
    client = get_servicebus_client()
    topic_name = get_topic_name()

    event = PubSubEvent(
        id=str(uuid.uuid4()),
        source="/my-application/events",
        type="com.example.event.v1",
        specversion="1.0",
        time=datetime.utcnow().isoformat() + "Z",
        data=event_data
    )

    sender = client.get_topic_sender(topic_name=topic_name)
    with sender:
        message = ServiceBusMessage(event.to_json())
        sender.send_messages(message)
    client.close()

    print(f"Published event with ID: {event.id} to topic: {topic_name}")

if __name__ == "__main__":
    # Example usage: Ensure AZURE_SERVICEBUS_CONNECTION_STRING and AZURE_SERVICEBUS_TOPIC_NAME are set in environment variables.
    example_event_data = {
        "eventType": "UserCreated",
        "userId": "user123",
        "userName": "John Doe",
        "email": "john.doe@example.com"
    }
    publish_event(example_event_data)
