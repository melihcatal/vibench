import json
from azure.servicebus import ServiceBusMessage
from messaging_client import MessagingClient
from messaging_models import ServiceBusConfig, EventMessage

def dead_letter_message(event_message: EventMessage, config: ServiceBusConfig, dead_letter_reason: str = "ProcessingFailed", dead_letter_error_description: str = "Message failed to process."):
    if not config.dead_letter_queue_name:
        raise ValueError("Dead letter queue name must be provided in config.")

    messaging_client = MessagingClient(config)
    sender = None
    try:
        sender = messaging_client.get_dead_letter_queue_sender()
        service_bus_message = ServiceBusMessage(
            json.dumps(event_message.event),
            message_id=event_message.message_id,
            content_type=event_message.content_type
        )
        # Azure Service Bus doesn't directly expose properties for dead-letter reason/description when *sending* a new message.
        # These are usually set when a message is automatically dead-lettered by the service or explicitly dead-lettered by a receiver.
        # For simulation purposes, we can add them as application properties.
        service_bus_message.application_properties["DeadLetterReason"] = dead_letter_reason
        service_bus_message.application_properties["DeadLetterErrorDescription"] = dead_letter_error_description

        with sender:
            sender.send_messages(service_bus_message)
        return {"status": "dead_lettered", "message_id": event_message.message_id}
    finally:
        if messaging_client:
            messaging_client.close()
