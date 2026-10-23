import os
from azure.servicebus import ServiceBusClient

def get_service_bus_client():
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
    return ServiceBusClient.from_connection_string(conn_str=connection_str)