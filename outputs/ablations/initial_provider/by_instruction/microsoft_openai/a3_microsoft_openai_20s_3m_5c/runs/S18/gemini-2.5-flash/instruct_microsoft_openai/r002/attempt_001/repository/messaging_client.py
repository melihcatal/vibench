from azure.servicebus import ServiceBusClient
import os

def get_service_bus_client() -> ServiceBusClient:
    """
    Provides a configured Azure Service Bus client.
    """
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")
    return ServiceBusClient.from_connection_string(connection_str)


def get_topic_name() -> str:
    """
    Retrieves the Azure Service Bus topic name from environment variables.
    """
    topic_name = os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME")
    if not topic_name:
        raise ValueError("AZURE_SERVICEBUS_TOPIC_NAME environment variable not set.")
    return topic_name


def get_subscription_name() -> str:
    """
    Retrieves the Azure Service Bus subscription name from environment variables.
    """
    subscription_name = os.environ.get("AZURE_SERVICEBUS_SUBSCRIPTION_NAME")
    if not subscription_name:
        raise ValueError("AZURE_SERVICEBUS_SUBSCRIPTION_NAME environment variable not set.")
    return subscription_name
