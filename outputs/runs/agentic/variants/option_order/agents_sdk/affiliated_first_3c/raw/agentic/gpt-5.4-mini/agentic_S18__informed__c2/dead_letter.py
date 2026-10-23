import json
import sys
from typing import Any, Dict

from azure.servicebus import ServiceBusMessage

from messaging_client import get_config, get_service_bus_client
from messaging_models import MessageEnvelope, PublishResponse, normalize_mapping, now_utc_iso


def dead_letter_message(message: Dict[str, Any]) -> PublishResponse:
    config = get_config()
    envelope = MessageEnvelope(
        message_id=str(message.get("message_id") or message.get("id") or now_utc_iso()),
        body=normalize_mapping(message.get("body") or message.get("payload") or message),
        attributes={**normalize_mapping(message.get("attributes")), "dead_letter": True},
    )
    with get_service_bus_client() as client:
        sender = client.get_queue_sender(queue_name=config.dead_letter_queue_name)
        with sender:
            sender.send_messages(
                ServiceBusMessage(
                    json.dumps(envelope.to_dict(), ensure_ascii=False),
                    message_id=envelope.message_id,
                    content_type=envelope.content_type,
                    application_properties=envelope.attributes,
                )
            )
    return PublishResponse(accepted=True, message_id=envelope.message_id, detail="sent to Azure Service Bus dead-letter queue")


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    message = json.loads(raw)
    response = dead_letter_message(message)
    print(json.dumps(response.__dict__))
