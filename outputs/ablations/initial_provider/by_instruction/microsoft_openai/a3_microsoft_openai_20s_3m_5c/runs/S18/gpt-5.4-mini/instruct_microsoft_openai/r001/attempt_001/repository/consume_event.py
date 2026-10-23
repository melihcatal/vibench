import json
from azure.servicebus import ServiceBusClient

from messaging_client import default_subscription, get_env, openai_endpoint
from messaging_models import ConsumptionResult, normalize_attributes


def consume_event(topic=None, subscription=None):
    conn_str = get_env("AZURE_SERVICEBUS_CONNECTION_STRING")
    topic_name = topic or get_env("MESSAGE_TOPIC", "pubsub-events")
    subscription_name = subscription or default_subscription()
    client = ServiceBusClient.from_connection_string(conn_str)
    with client:
        receiver = client.get_subscription_receiver(topic_name, subscription_name, max_wait_time=1)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=1)
            if not messages:
                return ConsumptionResult(None, "azure-servicebus", None, {}, None)
            message = messages[0]
            payload = json.loads(str(message))
            attributes = normalize_attributes(getattr(message, "application_properties", {}))
            return ConsumptionResult(getattr(message, "message_id", None), "azure-servicebus", payload, attributes, getattr(message, "lock_token", None))
