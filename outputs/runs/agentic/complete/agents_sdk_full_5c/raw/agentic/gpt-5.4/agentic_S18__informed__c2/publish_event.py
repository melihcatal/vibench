from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import build_servicebus_message, create_servicebus_client, get_queue_name, get_topic_name
from messaging_models import EventMessage, PublishResult, ensure_dict_payload


def publish_event(payload: Dict[str, Any], *, queue_name: Optional[str] = None, topic_name: Optional[str] = None, subject: Optional[str] = None, attributes: Optional[Dict[str, str]] = None) -> PublishResult:
    event = EventMessage(payload=ensure_dict_payload(payload), subject=subject, attributes=attributes or {})
    with create_servicebus_client() as client:
        if topic_name:
            destination = get_topic_name(topic_name)
            sender = client.get_topic_sender(topic_name=destination)
        else:
            destination = get_queue_name(queue_name)
            sender = client.get_queue_sender(queue_name=destination)
        with sender:
            message = build_servicebus_message(
                event.body_bytes(),
                message_id=event.message_id,
                subject=event.subject,
                application_properties=event.attributes,
                content_type=event.content_type,
            )
            sender.send_messages(message)
    return PublishResult(message_id=event.message_id, destination=destination, status="sent")
