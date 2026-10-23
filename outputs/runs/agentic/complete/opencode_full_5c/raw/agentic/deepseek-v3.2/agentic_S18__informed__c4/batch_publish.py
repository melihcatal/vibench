import json
import os
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def batch_publish(messages, topic_name="events"):
    """Publish a batch of messages with IDs to Azure Service Bus."""
    connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set"
        )

    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_topic_sender(topic_name) as sender:
            service_bus_messages = []
            results = []

            for msg in messages:
                message_id = str(uuid.uuid4())
                message_body = msg if isinstance(msg, dict) else {"data": msg}

                service_bus_message = ServiceBusMessage(
                    body=json.dumps(message_body).encode("utf-8"),
                    message_id=message_id,
                    content_type="application/json",
                    application_properties={
                        "batch_index": len(service_bus_messages),
                        "source": "batch_publisher",
                    },
                )
                service_bus_messages.append(service_bus_message)
                results.append({"message_id": message_id, "body": message_body})

            if service_bus_messages:
                sender.send_messages(service_bus_messages)

            return {
                "batch_size": len(results),
                "messages": results,
                "status": "batch_published",
            }
