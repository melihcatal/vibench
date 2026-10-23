import os
from azure.servicebus import ServiceBusClient


def get_servicebus_client():
    connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set."
        )
    return ServiceBusClient.from_connection_string(connection_string)
