import json
import os
from azure.servicebus import ServiceBusClient


def consume_event(topic_name="events", subscription_name="default"):
    """Consume one message from Azure Service Bus subscription."""
    connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "AZURE_SERVICE_BUS_CONNECTION_STRING environment variable not set"
        )

    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_subscription_receiver(
            topic_name=topic_name, subscription_name=subscription_name, max_wait_time=5
        ) as receiver:
            messages = receiver.receive_messages(max_message_count=1)
            if messages:
                message = messages[0]
                try:
                    body = json.loads(str(message))
                    receiver.complete_message(message)
                    return {
                        "message_id": message.message_id,
                        "body": body,
                        "status": "consumed",
                    }
                except Exception as e:
                    receiver.dead_letter_message(
                        message,
                        dead_letter_reason=str(e),
                        dead_letter_error_description="JSON parsing failed",
                    )
                    return {"error": str(e), "status": "dead-lettered"}
            return {"status": "no_messages"}
