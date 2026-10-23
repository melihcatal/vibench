from azure.servicebus import ServiceBusClient


def get_service_bus_client(connection_string):
    return ServiceBusClient.from_connection_string(connection_string)