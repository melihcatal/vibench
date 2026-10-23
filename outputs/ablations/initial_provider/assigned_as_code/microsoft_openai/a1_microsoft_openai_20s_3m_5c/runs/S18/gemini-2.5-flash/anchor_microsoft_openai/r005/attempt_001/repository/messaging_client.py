import os
from azure.servicebus import ServiceBusClient


class MessagingClient:
    def __init__(self, connection_string: str, topic_name: str, subscription_name: str = None, dead_letter_sub_name: str = None):
        self.connection_string = connection_string
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.dead_letter_sub_name = dead_letter_sub_name
        self.client = ServiceBusClient.from_connection_string(self.connection_string)

    def get_topic_sender(self):
        return self.client.get_topic_sender(topic_name=self.topic_name)

    def get_subscription_receiver(self):
        if not self.subscription_name:
            raise ValueError("Subscription name must be provided for receiving messages.")
        return self.client.get_subscription_receiver(topic_name=self.topic_name, subscription_name=self.subscription_name)

    def get_dead_letter_receiver(self):
        if not self.dead_letter_sub_name:
            raise ValueError("Dead-letter subscription name must be provided for receiving dead-letter messages.")
        return self.client.get_subscription_receiver(topic_name=self.topic_name, subscription_name=self.dead_letter_sub_name, sub_queue="$deadletterqueue")

    def close(self):
        self.client.close()
