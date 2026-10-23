import os
import json
from typing import Any

# Azure Service Bus integration
CONN_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


def send_to_dead_letter(
    topic_name: str, subscription_name: str, message_payload: Any
) -> None:
    """Send a failed message payload to the Service Bus dead-letter queue."""
    from azure.servicebus import ServiceBusClient, ServiceBusMessage

    client = ServiceBusClient.from_connection_string(CONN_STR)
    sender = client.get_topic_sender(topic_name)
    dlq_sender = client.get_dead_letter_sender(topic_name, subscription_name)
    # Wrap payload in a dict for proper JSON serialization
    dlq_message = ServiceBusMessage(
        json.dumps(message_payload), message_annotations={"dead_letter": True}
    )
    dlq_sender.send_messages(dlq_message)
