from __future__ import annotations

from typing import Any, Dict
import json
import uuid

from azure.servicebus import ServiceBusMessage

from messaging_client import get_client, load_config, build_message
from messaging_models import MessageEnvelope, PublishResult


def publish_event(payload: Dict[str, Any]) -> PublishResult:
    config = load_config()
    envelope = MessageEnvelope.from_mapping(payload)
    message = build_message(envelope.to_json(), envelope.id, envelope.content_type, **envelope.attributes)
    with get_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name)
        with sender:
            sender.send_messages(message)
    return PublishResult(message_id=envelope.id, succeeded=True, detail=config.topic_name)


if __name__ == "__main__":
    event = {"id": str(uuid.uuid4()), "type": "customer.created", "body": {"customer_id": "123", "plan": "pro"}}
    result = publish_event(event)
    print(json.dumps({"message_id": result.message_id, "succeeded": result.succeeded, "detail": result.detail}))
