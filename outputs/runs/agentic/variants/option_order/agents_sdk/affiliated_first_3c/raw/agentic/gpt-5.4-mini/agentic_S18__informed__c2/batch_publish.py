import json
import sys
from typing import Any, Dict, Iterable, List

from azure.servicebus import ServiceBusMessage

from messaging_client import get_config, get_service_bus_client
from messaging_models import MessageEnvelope, PublishResponse, normalize_messages, now_utc_iso


def batch_publish(events: Iterable[Dict[str, Any]]) -> PublishResponse:
    config = get_config()
    envelopes: List[MessageEnvelope] = normalize_messages(events)
    with get_service_bus_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name)
        with sender:
            messages = [
                ServiceBusMessage(
                    json.dumps({**envelope.to_dict(), "batch_id": now_utc_iso()}, ensure_ascii=False),
                    message_id=envelope.message_id,
                    content_type=envelope.content_type,
                    application_properties=envelope.attributes,
                )
                for envelope in envelopes
            ]
            sender.send_messages(messages)
    return PublishResponse(accepted=True, batch_count=len(envelopes), detail="batch sent to Azure Service Bus topic")


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "[]"
    events = json.loads(raw)
    response = batch_publish(events)
    print(json.dumps(response.__dict__))
