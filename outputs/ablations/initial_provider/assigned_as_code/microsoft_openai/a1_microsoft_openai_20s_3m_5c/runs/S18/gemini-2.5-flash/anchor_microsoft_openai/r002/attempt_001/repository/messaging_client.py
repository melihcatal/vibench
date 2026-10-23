from azure.servicebus import ServiceBusClient
import os

def get_servicebus_client(connection_string=None):
    if connection_string is None:
        connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("Azure Service Bus connection string not found.")
    return ServiceBusClient.from_connection_string(connection_string)
