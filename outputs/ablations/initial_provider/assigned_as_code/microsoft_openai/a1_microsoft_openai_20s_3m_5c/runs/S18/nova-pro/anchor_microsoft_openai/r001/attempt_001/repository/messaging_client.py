import os
from azure.servicebus import ServiceBusClient

def get_client():
    connection_str = os.getenv('AZURE_SERVICEBUS_CONNECTION_STRING')
    return ServiceBusClient.from_connection_string(connection_str)

def get_sender(client, topic_name):
    return client.get_topic_sender(topic_name)

def get_receiver(client, topic_name, subscription_name):
    return client.get_subscription_receiver(topic_name, subscription_name)