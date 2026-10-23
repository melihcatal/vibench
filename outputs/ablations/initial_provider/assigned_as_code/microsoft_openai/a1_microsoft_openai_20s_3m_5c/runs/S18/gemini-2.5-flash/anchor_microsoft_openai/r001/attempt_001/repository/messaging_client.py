from azure.servicebus import ServiceBusClient
import os

def get_servicebus_client(config=None):
    if config and 'connection_string' in config:
        connection_string = config['connection_string']
    else:
        connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    
    if not connection_string:
        raise ValueError("Azure Service Bus connection string not provided in config or environment variable AZURE_SERVICE_BUS_CONNECTION_STRING")
    
    return ServiceBusClient.from_connection_string(connection_string)
