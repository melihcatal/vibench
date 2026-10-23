import os
import json
from typing import Dict, Any

# Azure Service Bus integration
# Environment variable used for connection string
CONN_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


def consume_event(subscription_name: str, topic_name: str) -> Dict[str, Any]:
    """Consume a single message from the Service Bus subscription.
    Returns the deserialized JSON payload.
    """
    from azure.servicebus import ServiceBusClient, ServiceBusProcessor

    def on_message_received(msg_data):
        msg = msg_data.message
        payload = json.loads(msg.body)
        msg.complete()
        return payload

    def on_error(context):
        print(f"Error: {context}")

    client = ServiceBusClient.from_connection_string(CONN_STR)
    processor = ServiceBusProcessor(
        client=client,
        topic_name=topic_name,
        subscription_name=subscription_name,
        message_handler=on_message_received,
        error_handler=on_error,
    )
    processor.start()
    try:
        # Wait up to 10 seconds for a message
        payload = processor.receive_messages(max_wait_time=10)
        return next(payload, {})
    finally:
        processor.stop()
