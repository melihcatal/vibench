from __future__ import annotations

from typing import Any, Dict
import json

from messaging_client import MessagingConfig, build_servicebus_message, get_servicebus_client
from messaging_models import normalize_payload



def send_to_dead_letter(failed_message: Dict[str, Any], reason: str) -> Dict[str, Any]:
    config = MessagingConfig()
    payload = {
        "dead_letter_reason": reason,
        "failed_message": normalize_payload(failed_message),
    }
    body = json.dumps(payload)

    with get_servicebus_client(config) as client:
        sender = client.get_queue_sender(queue_name=config.dead_letter_queue_name)
        with sender:
            sender.send_messages(
                build_servicebus_message(
                    body,
                    application_properties={
                        "dead_letter_reason": reason,
                        "target": config.dead_letter_queue_name,
                    },
                )
            )

    return {
        "provider": "Azure Service Bus",
        "dead_letter_queue": config.dead_letter_queue_name,
        "status": "dead-lettered",
    }
