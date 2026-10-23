import json
import uuid
from azure.servicebus import ServiceBusMessage
from messaging_client import MessagingClient
from messaging_models import PublishResponse
import os


def batch_publish(payloads, config=None):
    config = config or {}
    connection_string = config.get('connection_string', os.environ.get('AZURE_SERVICEBUS_CONNECTION_STRING'))
    topic_name = config.get('topic_name', os.environ.get('AZURE_SERVICEBUS_TOPIC_NAME'))

    if not all([connection_string, topic_name]):
        raise ValueError("Missing Azure Service Bus configuration. Please provide connection_string and topic_name.")

    client = MessagingClient(connection_string, topic_name, "") # Subscription name not needed for publishing
    sender = client.get_topic_sender()

    message_ids = []
    with sender:
        message_batch = sender.create_message_batch()
        for payload in payloads:
            message_id = str(uuid.uuid4())
            message = ServiceBusMessage(
                json.dumps(payload['event']),
                message_id=message_id,
                content_type='application/json',
                application_properties=payload.get('attributes', {})
            )
            try:
                message_batch.add_message(message)
                message_ids.append(message_id)
            except ValueError:
                # Batch is full, send it and start a new one
                sender.send_message_batch(message_batch)
                message_batch = sender.create_message_batch()
                message_batch.add_message(message)
                message_ids.append(message_id)
        
        if message_batch:
            sender.send_message_batch(message_batch)
    
    client.close()
    return [PublishResponse(message_id=mid) for mid in message_ids]
