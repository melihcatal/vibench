import json
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def publish_event(event_data, topic_name="events"):
    """Publish a JSON event to Azure Service Bus topic."""
    connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set"
        )

    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_topic_sender(topic_name) as sender:
            message = ServiceBusMessage(
                body=json.dumps(event_data).encode("utf-8"),
                content_type="application/json",
            )
            sender.send_messages(message)
            return {"message_id": message.message_id, "status": "published"}
