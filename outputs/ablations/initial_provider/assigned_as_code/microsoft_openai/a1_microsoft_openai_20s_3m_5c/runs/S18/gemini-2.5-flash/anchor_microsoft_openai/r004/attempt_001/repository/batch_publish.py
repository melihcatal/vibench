import json
from azure.servicebus import ServiceBusMessage, ServiceBusMessageBatch
from messaging_client import MessagingClient
from messaging_models import ServiceBusConfig, EventMessage
from typing import List

def batch_publish_events(event_messages: List[EventMessage], config: ServiceBusConfig):
    if not config.topic_name and not config.queue_name:
        raise ValueError("Topic name or Queue name must be provided in config.")

    messaging_client = MessagingClient(config)
    sender = None
    results = []
    try:
        if config.topic_name:
            sender = messaging_client.get_topic_sender()
        elif config.queue_name:
            sender = messaging_client.get_queue_sender()

        with sender:
            batch = sender.create_message_batch()
            for event_message in event_messages:
                service_bus_message = ServiceBusMessage(
                    json.dumps(event_message.event),
                    message_id=event_message.message_id,
                    content_type=event_message.content_type
                )
                try:
                    batch.add_message(service_bus_message)
                except ValueError: # Batch is full
                    # Send the current batch and start a new one
                    sender.send_messages(batch)
                    results.append({"status": "published_batch", "count": len(batch)})
                    batch = sender.create_message_batch()
                    batch.add_message(service_bus_message)
            
            if batch:
                sender.send_messages(batch)
                results.append({"status": "published_batch", "count": len(batch)})

        return results
    finally:
        if messaging_client:
            messaging_client.close()
