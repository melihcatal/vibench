from azure.servicebus import ServiceBusMessage

def create_service_bus_message(content):
    return ServiceBusMessage(content)