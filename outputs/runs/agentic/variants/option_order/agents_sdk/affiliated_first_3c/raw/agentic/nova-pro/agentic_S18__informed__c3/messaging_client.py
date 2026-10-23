import os
from azure.servicebus import ServiceBusClient

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'your_connection_string'

def get_service_bus_client():
    return ServiceBusClient.from_connection_string(os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING'))