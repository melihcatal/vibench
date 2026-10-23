import json
import sys
from typing import Any, Dict

from azure.servicebus import ServiceBusMessage

from messaging_client import get_config, get_service_bus_client
from messaging_models import MessageEnvelope, PublishResponse, normalize_mapping, now_utc_iso


def publish_event(event: Dict[str, Any]) -> PublishResponse:
    config = get_config()
    envelope = MessageEnvelope(
        message_id=str(event.get("message_id") or event.get("id") or now_utc_iso()),
        body=normalize_mapping(event.get("body") or event.get("payload") or event),
        attributes=normalize_mapping(event.get("attributes")),
    )
    with get_service_bus_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name)
        with sender:
            sender.send_messages(
                ServiceBusMessage(
                    json.dumps(envelope.to_dict(), ensure_ascii=False),
                    message_id=envelope.message_id,
                    content_type=envelope.content_type,
                    application_properties=envelope.attributes,
                )
            )
    return PublishResponse(accepted=True, message_id=envelope.message_id, detail="sent to Azure Service Bus topic")


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    event = json.loads(raw)
    response = publish_event(event)
    print(json.dumps(response.__dict__))
