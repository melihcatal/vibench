from __future__ import annotations

from typing import Optional
import json

from messaging_client import get_client, load_config
from messaging_models import ConsumeResult, extract_json_payload


def consume_event() -> Optional[ConsumeResult]:
    config = load_config()
    with get_client() as client:
        receiver = client.get_subscription_receiver(topic_name=config.topic_name, subscription_name=config.subscription_name, max_wait_time=5)
        with receiver:
            messages = list(receiver.receive_messages(max_message_count=1, max_wait_time=5))
            if not messages:
                return None
            message = messages[0]
            body_text = str(message)
            payload = extract_json_payload(body_text)
            receiver.complete_message(message)
            return ConsumeResult(message_id=str(getattr(message, "message_id", "")), body=payload, attributes=dict(getattr(message, "application_properties", {}) or {}), raw=message)


if __name__ == "__main__":
    result = consume_event()
    print(json.dumps({"message_id": getattr(result, "message_id", None), "body": getattr(result, "body", None)}))
