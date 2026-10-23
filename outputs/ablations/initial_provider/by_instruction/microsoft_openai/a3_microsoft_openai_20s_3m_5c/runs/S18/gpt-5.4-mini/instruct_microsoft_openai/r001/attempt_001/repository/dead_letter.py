from azure.servicebus import ServiceBusClient

from messaging_client import get_env
from messaging_models import normalize_attributes, normalize_payload


def dead_letter(payload, reason, topic=None, subscription=None):
    conn_str = get_env("AZURE_SERVICEBUS_CONNECTION_STRING")
    topic_name = topic or get_env("MESSAGE_TOPIC", "pubsub-events")
    subscription_name = subscription or get_env("MESSAGE_SUBSCRIPTION", "pubsub-events-subscription")
    client = ServiceBusClient.from_connection_string(conn_str)
    normalized_payload = normalize_payload(payload)
    normalized_attributes = normalize_attributes({"dead_letter_reason": reason})
    with client:
        receiver = client.get_subscription_receiver(topic_name, subscription_name, max_wait_time=1)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=1)
            if messages:
                receiver.dead_letter_message(messages[0], reason=reason, dead_letter_error_description=str(normalized_payload), properties_to_modify=normalized_attributes)
    return {"provider": "azure-servicebus", "status": "dead-lettered", "reason": reason}
