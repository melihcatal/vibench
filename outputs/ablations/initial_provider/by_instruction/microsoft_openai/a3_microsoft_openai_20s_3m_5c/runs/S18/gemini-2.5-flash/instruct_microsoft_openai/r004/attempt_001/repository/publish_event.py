import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_models import Event

def publish_event(event: Event):
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    queue_name = os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME", "myqueue")

    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        with client.get_queue_sender(queue_name) as sender:
            message_body = json.dumps(event.dict())
            message = ServiceBusMessage(message_body)
            sender.send_messages(message)
            print(f"Sent message: {message_body}")

if __name__ == "__main__":
    # Example usage (replace with actual event data)
    example_event = Event(id="123", type="user_created", data={"name": "John Doe", "email": "john.doe@example.com"})
    publish_event(example_event)
