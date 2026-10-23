import os
from azure.servicebus import ServiceBusClient

# Azure Service Bus configuration
CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


def get_servicebus_client():
    return ServiceBusClient.from_connection_string(CONNECTION_STR)


def create_message(content):
    return ServiceBusMessage(content)
