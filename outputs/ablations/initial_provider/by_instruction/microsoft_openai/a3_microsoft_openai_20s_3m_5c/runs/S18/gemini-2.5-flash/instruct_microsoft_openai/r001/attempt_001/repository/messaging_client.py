import os
from azure.servicebus import ServiceBusClient

class MessagingClient:
    def __init__(self, connection_str: str, queue_name: str | None = None, topic_name: str | None = None, subscription_name: str | None = None):
        self.connection_str = connection_str
        self.queue_name = queue_name
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.client = ServiceBusClient.from_connection_string(self.connection_str)

    def get_sender(self):
        if self.topic_name:
            return self.client.get_topic_sender(topic_name=self.topic_name)
        elif self.queue_name:
            return self.client.get_queue_sender(queue_name=self.queue_name)
        else:
            raise ValueError("Either queue_name or topic_name must be provided for sender.")

    def get_receiver(self):
        if self.queue_name:
            return self.client.get_queue_receiver(queue_name=self.queue_name)
        elif self.topic_name and self.subscription_name:
            return self.client.get_subscription_receiver(topic_name=self.topic_name, subscription_name=self.subscription_name)
        else:
            raise ValueError("Either queue_name or topic_name with subscription_name must be provided for receiver.")

    def close(self):
        self.client.close()

def get_service_bus_client(queue_name: str | None = None, topic_name: str | None = None, subscription_name: str | None = None) -> MessagingClient:
    connection_str = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set.")
    return MessagingClient(connection_str, queue_name, topic_name, subscription_name)
