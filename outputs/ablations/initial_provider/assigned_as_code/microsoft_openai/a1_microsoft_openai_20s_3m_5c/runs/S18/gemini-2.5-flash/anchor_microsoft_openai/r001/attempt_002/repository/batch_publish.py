import json
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import get_service_bus_connection_string
from messaging_models import BatchPublishRequest, BatchPublishResponse

def batch_publish_events(topic_name: str, batch_request: BatchPublishRequest):
    connection_string = get_service_bus_connection_string()
    message_ids = []
    with ServiceBusClient.from_connection_string(connection_string) as servicebus_client:
        with servicebus_client.get_topic_sender(topic_name=topic_name) as sender:
            message_batch = sender.create_message_batch()
            for event_payload in batch_request.events:
                message_id = str(uuid.uuid4())
                message = ServiceBusMessage(json.dumps(event_payload), message_id=message_id, content_type='application/json')
                try:
                    message_batch.add_message(message)
                    message_ids.append(message_id)
                except ValueError:
                    # Batch is full, send it and create a new one
                    sender.send_message_batch(message_batch)
                    message_batch = sender.create_message_batch()
                    message_batch.add_message(message)
                    message_ids.append(message_id)
            if message_batch:
                sender.send_message_batch(message_batch)
    return BatchPublishResponse(message_ids=message_ids)
