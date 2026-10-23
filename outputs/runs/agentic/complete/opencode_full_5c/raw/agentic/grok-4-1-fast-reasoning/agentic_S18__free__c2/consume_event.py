from typing import Dict, Any, Optional
from messaging_client import pull_one_message, ack_message
from messaging_models import PubSubMessage


def consume_event() -> Optional[Dict[str, Any]]:
    msg = pull_one_message()
    if msg:
        payload = msg.payload()
        ack_message(msg)
        return payload
    return None
