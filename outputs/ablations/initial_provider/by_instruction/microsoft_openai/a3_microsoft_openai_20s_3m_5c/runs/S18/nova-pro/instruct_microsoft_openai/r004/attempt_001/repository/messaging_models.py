from azure.servicebus import ServiceBusMessage

def create_message(content):
    return ServiceBusMessage(content)

def extract_message_body(message):
    return message.body