from __future__ import annotations

from typing import Any, Dict
import json

from messaging_client import MessagingConfig, build_servicebus_message, get_servicebus_client
from messaging_models import PublishEventRequest, normalize_payload



def publish_event(event: Dict[str, Any]) -> Dict[str, Any]:
    config = MessagingConfig()
    request = PublishEventRequest(body=normalize_payload(event))
    message_body = request.to_message_body()
    payload = json.loads(message_body)

    with get_servicebus_client(config) as client:
        sender = client.get_queue_sender(queue_name=config.queue_name)
        with sender:
            sender.send_messages(
                build_servicebus_message(
                    message_body,
                    message_id=payload["message_id"],
                    application_properties=request.attributes.to_headers(),
                )
            )

    return {
        "provider": "Azure Service Bus",
        "queue": config.queue_name,
        "message_id": payload["message_id"],
        "status": "published",
    }
