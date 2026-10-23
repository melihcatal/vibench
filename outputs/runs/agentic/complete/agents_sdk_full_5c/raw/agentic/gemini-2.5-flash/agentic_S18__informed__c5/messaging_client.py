import os
from azure.servicebus import ServiceBusClient

def get_service_bus_client() -> ServiceBusClient:
    """Returns a configured Azure Service Bus client."""
    connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set.")
    
    return ServiceBusClient.from_connection_string(conn_str=connection_string)

