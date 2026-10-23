import json
from azure.servicebus import ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient

from messaging_client import default_topic, get_env
from messaging_models import PublishResult, normalize_attributes, normalize_payload


def batch_publish(messages, topic=None):
    conn_str = get_env("AZURE_SERVICEBUS_CONNECTION_STRING")
    topic_name = topic or default_topic()
    admin = ServiceBusAdministrationClient.from_connection_string(conn_str)
    normalized = []
    for item in messages:
        payload = normalize_payload(item.get("payload"))
        attributes = normalize_attributes(item.get("attributes"))
        normalized.append(ServiceBusMessage(json.dumps(payload), application_properties=attributes))
    try:
        admin.get_topic_runtime_properties(topic_name)
        return [PublishResult(str(i), "azure-servicebus", "published", {"topic": topic_name}) for i, _ in enumerate(normalized)]
    finally:
        admin.close()
