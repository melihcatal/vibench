from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import get_servicebus_client
import json
import os

def send_to_dead_letter(original_message_payload, dead_letter_topic_name=None, dead_letter_queue_name=None, error_details=None):
    connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    client = get_servicebus_client(connection_string)
    
    if not (dead_letter_topic_name or dead_letter_queue_name):
        raise ValueError("Either dead_letter_topic_name or dead_letter_queue_name must be provided.")

    if dead_letter_topic_name:
        sender = client.get_topic_sender(topic_name=dead_letter_topic_name)
    elif dead_letter_queue_name:
        sender = client.get_queue_sender(queue_name=dead_letter_queue_name)

    with sender:
        message_body = original_message_payload.get("body", "{}")
        message_id = original_message_payload.get("message_id")
        content_type = original_message_payload.get("content_type", "application/json")
        attributes = original_message_payload.get("attributes", {})

        # Add error details to attributes or body for dead-lettering context
        if error_details:
            attributes["deadLetterError"] = json.dumps(error_details)

        dead_letter_message = ServiceBusMessage(
            json.dumps(message_body) if content_type == "application/json" else message_body,
            message_id=message_id,
            content_type=content_type,
            application_properties=attributes
        )
        sender.send_messages(dead_letter_message)
    return {"status": "sent_to_dead_letter", "message_id": message_id}
