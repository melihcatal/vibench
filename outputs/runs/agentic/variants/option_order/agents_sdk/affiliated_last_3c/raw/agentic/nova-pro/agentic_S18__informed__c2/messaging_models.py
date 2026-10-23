from azure.servicebus import ServiceBusMessage

def create_message(data):
    return ServiceBusMessage(data)