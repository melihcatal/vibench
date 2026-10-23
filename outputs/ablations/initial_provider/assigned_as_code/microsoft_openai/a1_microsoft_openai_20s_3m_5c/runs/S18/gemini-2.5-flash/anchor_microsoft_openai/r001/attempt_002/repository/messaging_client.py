import os
from azure.servicebus import ServiceBusClient

def get_service_bus_client(connection_string: str) -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(connection_string)

def get_service_bus_connection_string() -> str:
    conn_str = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set.")
    return conn_str
