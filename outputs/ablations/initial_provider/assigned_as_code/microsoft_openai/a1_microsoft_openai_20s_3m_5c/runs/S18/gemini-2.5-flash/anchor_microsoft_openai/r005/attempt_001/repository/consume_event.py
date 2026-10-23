import json
import os
from messaging_client import MessagingClient
from messaging_models import EventMessage
from azure.servicebus import ServiceBusMessage

def consume_event(config=None):
    config = config or {}
    connection_string = config.get('connection_string', os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING"))
    topic_name = config.get('topic_name', os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME"))
    subscription_name = config.get('subscription_name', os.environ.get("AZURE_SERVICEBUS_SUBSCRIPTION_NAME"))

    if not all([connection_string, topic_name, subscription_name]):
        raise ValueError("Azure Service Bus connection string, topic name, and subscription name must be provided.")

    client = MessagingClient(
        connection_string=connection_string,
        topic_name=topic_name,
        subscription_name=subscription_name
    )

    received_message = None
    try:
        with client.get_subscription_receiver() as receiver:
            for msg in receiver:
                print(f"Received message: {msg.sequence_number}")
                data = json.loads(str(msg))
                received_message = EventMessage(
                    event_id=msg.message_id,
                    event_type=data.get("event_type"),
                    data=data,
                    attributes={key: str(value) for key, value in msg.application_properties.items()} if msg.application_properties else {}
                )
                receiver.complete_message(msg)
                break  # Process one message at a time for this function
    finally:
        client.close()

    return received_message
