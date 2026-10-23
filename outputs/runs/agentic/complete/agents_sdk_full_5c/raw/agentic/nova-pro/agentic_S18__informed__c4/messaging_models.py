from azure.servicebus import ServiceBusMessage

def create_servicebus_message(content):
    return ServiceBusMessage(content)