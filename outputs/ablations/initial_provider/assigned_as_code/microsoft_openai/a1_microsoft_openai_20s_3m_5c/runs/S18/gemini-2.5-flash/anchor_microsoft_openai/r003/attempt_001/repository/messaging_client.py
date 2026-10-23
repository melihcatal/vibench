from azure.servicebus import ServiceBusClient
import os


class MessagingClient:
    def __init__(self, connection_string: str, topic_name: str, subscription_name: str):
        self.connection_string = connection_string
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.servicebus_client = ServiceBusClient.from_connection_string(self.connection_string)

    def get_topic_sender(self):
        return self.servicebus_client.get_topic_sender(topic_name=self.topic_name)

    def get_subscription_receiver(self):
        return self.servicebus_client.get_subscription_receiver(topic_name=self.topic_name, subscription_name=self.subscription_name)

    def get_dead_letter_receiver(self):
        # For dead-letter queue, the subscription name gets appended with /$DeadLetterQueue
        dead_letter_subscription_name = f"{self.subscription_name}/$DeadLetterQueue"
        return self.servicebus_client.get_subscription_receiver(topic_name=self.topic_name, subscription_name=dead_letter_subscription_name)

    def close(self):
        self.servicebus_client.close()
