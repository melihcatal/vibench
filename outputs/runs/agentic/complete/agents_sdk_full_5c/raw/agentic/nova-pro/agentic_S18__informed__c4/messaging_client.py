import os
from azure.servicebus import ServiceBusClient

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=your-policy-name;SharedAccessKey=your-policy-key'

def get_servicebus_client():
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
    return ServiceBusClient.from_connection_string(conn_str=connection_str)