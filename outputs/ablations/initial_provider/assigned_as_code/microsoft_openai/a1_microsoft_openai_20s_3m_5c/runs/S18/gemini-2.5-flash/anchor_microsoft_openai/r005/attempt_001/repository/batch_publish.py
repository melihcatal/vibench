import json
import os
from messaging_client import MessagingClient
from messaging_models import EventMessage, BatchEvent, MessageResult
from azure.servicebus import ServiceBusMessage

def batch_publish(batch_event: BatchEvent, config=None):
    config = config or {}
    connection_string = config.get('connection_string', os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING"))
    topic_name = config.get('topic_name', os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME"))

    if not all([connection_string, topic_name]):
        raise ValueError("Azure Service Bus connection string and topic name must be provided.")

    client = MessagingClient(
        connection_string=connection_string,
        topic_name=topic_name
    )

    results = []
    try:
        with client.get_topic_sender() as sender:
            service_bus_messages = []
            for event_msg in batch_event.messages:
                message_body = json.dumps(event_msg.data)
                sb_message = ServiceBusMessage(
                    message_body,
                    message_id=event_msg.event_id,
                    content_type='application/json',
                    application_properties=event_msg.attributes
                )
                service_bus_messages.append(sb_message)

            if service_bus_messages:
                sender.send_messages(service_bus_messages)
                for event_msg in batch_event.messages:
                    results.append(MessageResult(message_id=event_msg.event_id, status="published"))
    finally:
        client.close()

    return results
