from azure.servicebus import ServiceBusMessage


class EventMessage:
    def __init__(self, content):
        self.content = content

    def to_servicebus_message(self):
        return ServiceBusMessage(self.content)


class ProcessedMessage:
    def __init__(self, content, status):
        self.content = content
        self.status = status
