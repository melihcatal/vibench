from __future__ import annotations

from typing import Optional

from messaging_client import pubsub_post, subscription_path
from messaging_models import ConsumedMessage, normalize_pubsub_message


def consume_event(auto_ack: bool = False) -> Optional[ConsumedMessage]:
    subscription = subscription_path()
    response = pubsub_post(f"{subscription}:pull", {"maxMessages": 1})
    messages = response.get("receivedMessages", [])
    if not messages:
        return None
    consumed = normalize_pubsub_message(messages[0])
    if auto_ack and consumed.ack_id:
        pubsub_post(f"{subscription}:acknowledge", {"ackIds": [consumed.ack_id]})
    return consumed
