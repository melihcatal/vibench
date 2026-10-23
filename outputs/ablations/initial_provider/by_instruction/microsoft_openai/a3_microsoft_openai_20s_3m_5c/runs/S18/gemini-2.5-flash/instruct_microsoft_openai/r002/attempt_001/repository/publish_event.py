from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import json

def publish_event(topic_name: str, event_data: dict):
    """
    Publishes a JSON event to an Azure Service Bus topic.
    """
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_topic_sender(topic_name=topic_name)
        with sender:
            message = ServiceBusMessage(json.dumps(event_data))
            sender.send_messages(message)
            print(f"Sent message to topic: {topic_name}")

if __name__ == "__main__":
    # Example usage (for demonstration, in a real scenario this would be called by another module)
    # Ensure AZURE_SERVICEBUS_CONNECTION_STRING and AZURE_SERVICEBUS_TOPIC_NAME are set in your environment
    sample_event = {"id": "123", "type": "OrderCreated", "data": {"item": "Book", "quantity": 1}}
    topic = os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME", "my_topic")
    publish_event(topic, sample_event)
