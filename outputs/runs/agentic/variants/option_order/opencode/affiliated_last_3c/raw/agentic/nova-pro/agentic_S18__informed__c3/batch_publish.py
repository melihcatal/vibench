import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Azure Service Bus configuration
CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = "your-queue-name"


def batch_publish(events):
    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        sender = client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            messages = [ServiceBusMessage(event) for event in events]
            sender.send_messages(messages)


if __name__ == "__main__":
    events = [{"key": "value1"}, {"key": "value2"}]
    batch_publish(events)
