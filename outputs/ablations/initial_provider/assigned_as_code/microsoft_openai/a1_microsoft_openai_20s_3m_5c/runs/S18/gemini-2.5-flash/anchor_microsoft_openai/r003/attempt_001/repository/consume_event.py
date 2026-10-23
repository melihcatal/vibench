import json
from messaging_client import MessagingClient
from messaging_models import ConsumeResponse
import os


def consume_event(config=None):
    config = config or {}
    connection_string = config.get('connection_string', os.environ.get('AZURE_SERVICEBUS_CONNECTION_STRING'))
    topic_name = config.get('topic_name', os.environ.get('AZURE_SERVICEBUS_TOPIC_NAME'))
    subscription_name = config.get('subscription_name', os.environ.get('AZURE_SERVICEBUS_SUBSCRIPTION_NAME'))

    if not all([connection_string, topic_name, subscription_name]):
        raise ValueError("Missing Azure Service Bus configuration. Please provide connection_string, topic_name, and subscription_name.")

    client = MessagingClient(connection_string, topic_name, subscription_name)
    receiver = client.get_subscription_receiver()

    message = receiver.receive_messages(max_wait_time=5)[0] # Receive a single message
    if message:
        payload = json.loads(str(message))
        response = ConsumeResponse(
            message_id=message.message_id,
            payload=payload,
            attributes={k: v for k, v in message.application_properties.items()} if message.application_properties else {},
            sequence_number=message.sequence_number
        )
        receiver.complete_message(message)
        client.close()
        return response
    client.close()
    return None
