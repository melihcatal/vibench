from typing import Mapping

from google.cloud import pubsub_v1

from messaging_models import summarize_attributes


def summarize_message(message_id: str, payload: Mapping[str, object], attributes: Mapping[str, str], status: str) -> str:
    attr_text = summarize_attributes(attributes)
    payload_keys = ", ".join(sorted(payload.keys()))
    return f"message_id={message_id}; status={status}; payload_keys=[{payload_keys}]; attributes=[{attr_text}]"
