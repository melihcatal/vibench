import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import get_service_bus_client

def publish_event(topic_name: str, event_data: dict):
    """Publishes a JSON event to an Azure Service Bus topic."""
    servicebus_client = get_service_bus_client()
    sender = servicebus_client.get_topic_sender(topic_name=topic_name)

    with sender:
        message = ServiceBusMessage(json.dumps(event_data))
        sender.send_messages(message)
        print(f"Published event to topic '{topic_name}': {event_data}")

if __name__ == '__main__':
    # Example usage (replace with actual topic name and event data)
    topic = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")
    example_event = {"id": "123", "type": "user_created", "payload": {"username": "testuser"}}
    publish_event(topic, example_event)
