import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Configuration
SERVICE_BUS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
TOPIC_NAME = "your-topic-name"


# Publish a batch of messages with IDs or attributes
def batch_publish(events):
    with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STR) as client:
        sender = client.get_topic_sender(TOPIC_NAME)
        messages = [ServiceBusMessage(event) for event in events]
        sender.send_messages(messages)


if __name__ == "__main__":
    events = ['{"key": "value1"}', '{"key": "value2"}']
    batch_publish(events)
