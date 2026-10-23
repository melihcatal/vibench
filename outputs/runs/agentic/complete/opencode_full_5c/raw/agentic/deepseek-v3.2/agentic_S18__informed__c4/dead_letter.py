import json
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def dead_letter(message_body, error_reason, dlq_topic_name="dead-letter"):
    """Send failed messages to Azure Service Bus dead-letter queue."""
    connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set"
        )

    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_topic_sender(dlq_topic_name) as sender:
            dead_letter_message = {
                "original_body": message_body,
                "error_reason": error_reason,
                "timestamp": os.path.getctime(__file__)
                if os.path.exists(__file__)
                else None,
            }

            message = ServiceBusMessage(
                body=json.dumps(dead_letter_message).encode("utf-8"),
                content_type="application/json",
                application_properties={
                    "dead_letter_reason": error_reason,
                    "source": "dead_letter_handler",
                },
            )
            sender.send_messages(message)
            return {"message_id": message.message_id, "status": "dead_lettered"}
