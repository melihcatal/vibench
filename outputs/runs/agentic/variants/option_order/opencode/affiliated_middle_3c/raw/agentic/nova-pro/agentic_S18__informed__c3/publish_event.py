import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Configuration
SERVICE_BUS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
TOPIC_NAME = "your-topic-name"


# Publish a JSON event to a managed messaging topic
def publish_event(event):
    with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STR) as client:
        sender = client.get_topic_sender(TOPIC_NAME)
        message = ServiceBusMessage(event)
        sender.send_messages(message)


if __name__ == "__main__":
    event = '{"key": "value"}'
    publish_event(event)
