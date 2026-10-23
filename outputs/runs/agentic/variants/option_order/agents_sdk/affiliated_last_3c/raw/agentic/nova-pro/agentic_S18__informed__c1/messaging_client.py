import os
from azure.servicebus import ServiceBusClient

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>'

connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')

def get_client():
    return ServiceBusClient.from_connection_string(connection_str)