import json
from azure.servicebus import ServiceBusClient
from messaging_client import get_service_bus_connection_string
from messaging_models import ConsumeResponse

def consume_dead_letter_event(queue_name: str):
    connection_string = get_service_bus_connection_string()
    dead_letter_queue_name = f"{queue_name}/$deadletterqueue"
    with ServiceBusClient.from_connection_string(connection_string) as servicebus_client:
        with servicebus_client.get_queue_receiver(queue_name=dead_letter_queue_name) as receiver:
            for msg in receiver:
                message_body = str(msg.body)
                message_id = msg.message_id
                properties = {
                    "content_type": msg.content_type,
                    "sequence_number": msg.sequence_number,
                    "time_to_live": msg.time_to_live,
                    "enqueued_time_utc": msg.enqueued_time_utc.isoformat(),
                    "dead_letter_reason": msg.dead_letter_reason,
                    "dead_letter_error_description": msg.dead_letter_error_description
                }
                receiver.complete_message(msg)
                return ConsumeResponse(message_id=message_id, body=message_body, properties=properties)
    return None
