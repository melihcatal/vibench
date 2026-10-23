from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import get_servicebus_client
import json
import os

def batch_publish(messages, topic_name):
    connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    client = get_servicebus_client(connection_string)
    sender = client.get_topic_sender(topic_name=topic_name)

    with sender:
        service_bus_messages = []
        for msg_payload in messages:
            message_body = msg_payload.get("body", {})
            message_id = msg_payload.get("message_id")
            content_type = msg_payload.get("content_type", "application/json")
            attributes = msg_payload.get("attributes", {})

            sb_message = ServiceBusMessage(
                json.dumps(message_body) if content_type == "application/json" else message_body,
                message_id=message_id,
                content_type=content_type,
                application_properties=attributes
            )
            service_bus_messages.append(sb_message)
        
        if service_bus_messages:
            sender.send_messages(service_bus_messages)
    
    return {"status": "batch_published", "count": len(messages)}
