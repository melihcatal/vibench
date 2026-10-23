import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Azure Service Bus configuration
CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = "your-queue-name"


def publish_event(event):
    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        sender = client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            sender.send_messages(ServiceBusMessage(event))


if __name__ == "__main__":
    event = {"key": "value"}
    publish_event(event)
