from azure.servicebus import ServiceBusMessage

class EventMessage(ServiceBusMessage):
    def __init__(self, body, **kwargs):
        super().__init__(body, **kwargs)