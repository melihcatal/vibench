import os
from azure.servicebus import ServiceBusClient

def get_servicebus_client():
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")
    return ServiceBusClient.from_connection_string(connection_str)

def get_queue_name():
    return os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME", "myqueue")
