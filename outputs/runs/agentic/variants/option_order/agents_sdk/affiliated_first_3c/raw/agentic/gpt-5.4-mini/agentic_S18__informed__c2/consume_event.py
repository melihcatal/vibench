import json
from typing import Any, Dict

from messaging_client import get_config, get_service_bus_client
from messaging_models import ConsumeResponse, normalize_mapping


def consume_event() -> ConsumeResponse:
    config = get_config()
    with get_service_bus_client() as client:
        receiver = client.get_subscription_receiver(topic_name=config.topic_name, subscription_name=config.subscription_name)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return ConsumeResponse(message_id=None, body={}, attributes={}, delivery_count=0)
            message = messages[0]
            body: Dict[str, Any]
            try:
                body = json.loads(str(message))
            except Exception:
                body = {"raw": str(message)}
            return ConsumeResponse(
                message_id=getattr(message, "message_id", None),
                body=body,
                attributes=normalize_mapping(getattr(message, "application_properties", {})),
                delivery_count=getattr(message, "delivery_count", 0),
                locked_until_utc=str(getattr(message, "locked_until_utc", "")) or None,
            )
