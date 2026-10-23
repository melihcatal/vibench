from azure.servicebus import ServiceBusMessage


# Define local request, response, and normalization helpers for Pub/Sub Messaging
class MessagingModels:
    @staticmethod
    def create_message(content):
        return ServiceBusMessage(content)
