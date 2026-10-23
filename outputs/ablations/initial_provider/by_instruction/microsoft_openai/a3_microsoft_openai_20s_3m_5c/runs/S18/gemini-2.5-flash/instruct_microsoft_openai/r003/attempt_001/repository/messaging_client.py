import os
from azure.servicebus import ServiceBusClient, ServiceBusSender

class MessagingClient:
    def __init__(self):
        self.connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
        if not self.connection_str:
            raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    def get_sender(self, topic_name: str) -> ServiceBusSender:
        servicebus_client = ServiceBusClient.from_connection_string(self.connection_str)
        sender = servicebus_client.get_topic_sender(topic_name)
        return sender
