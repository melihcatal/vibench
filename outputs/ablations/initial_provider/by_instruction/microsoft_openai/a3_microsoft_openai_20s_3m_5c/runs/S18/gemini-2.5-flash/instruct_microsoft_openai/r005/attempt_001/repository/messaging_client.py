import os
from azure.servicebus import ServiceBusClient

def get_servicebus_client() -> ServiceBusClient:
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")
    return ServiceBusClient.from_connection_string(connection_str)

def get_topic_name() -> str:
    topic_name = os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME")
    if not topic_name:
        raise ValueError("AZURE_SERVICEBUS_TOPIC_NAME environment variable not set.")
    return topic_name

def get_queue_name() -> str:
    queue_name = os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME")
    if not queue_name:
        raise ValueError("AZURE_SERVICEBUS_QUEUE_NAME environment variable not set.")
    return queue_name

def get_subscription_name() -> str:
    subscription_name = os.environ.get("AZURE_SERVICEBUS_SUBSCRIPTION_NAME")
    if not subscription_name:
        raise ValueError("AZURE_SERVICEBUS_SUBSCRIPTION_NAME environment variable not set.")
    return subscription_name
