import os
from azure.servicebus import ServiceBusClient

# Configuration
SERVICE_BUS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


# Provide local configuration and client helper utilities for Pub/Sub Messaging
class MessagingClient:
    def __init__(self):
        self.client = ServiceBusClient.from_connection_string(
            SERVICE_BUS_CONNECTION_STR
        )

    def get_topic_sender(self, topic_name):
        return self.client.get_topic_sender(topic_name)

    def get_subscription_receiver(self, topic_name, subscription_name):
        return self.client.get_subscription_receiver(topic_name, subscription_name)

    def get_queue_sender(self, queue_name):
        return self.client.get_queue_sender(queue_name)
