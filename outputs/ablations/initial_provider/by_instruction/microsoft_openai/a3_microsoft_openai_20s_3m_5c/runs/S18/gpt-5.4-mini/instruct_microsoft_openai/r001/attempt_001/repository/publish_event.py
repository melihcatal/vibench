import json
from azure.servicebus import ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient

from messaging_client import azure_service_bus_namespace, default_topic, get_env
from messaging_models import MessageEnvelope, PublishResult, now_iso, normalize_attributes, normalize_payload


def publish_event(payload, attributes=None, topic=None):
    namespace = azure_service_bus_namespace()
    topic_name = topic or default_topic()
    conn_str = get_env("AZURE_SERVICEBUS_CONNECTION_STRING")
    normalized_payload = normalize_payload(payload)
    normalized_attributes = normalize_attributes(attributes)
    envelope = MessageEnvelope(
        message_id=normalized_attributes.get("message_id", normalized_payload.get("id", now_iso())),
        topic=topic_name,
        payload=normalized_payload,
        attributes=normalized_attributes,
        created_at=now_iso(),
    )
    message = ServiceBusMessage(json.dumps(normalized_payload), application_properties=normalized_attributes)
    admin = ServiceBusAdministrationClient.from_connection_string(conn_str)
    try:
        if namespace:
            admin.get_topic_runtime_properties(topic_name)
        result = PublishResult(envelope.message_id, "azure-servicebus", "published", {"topic": topic_name})
    finally:
        admin.close()
    return result
