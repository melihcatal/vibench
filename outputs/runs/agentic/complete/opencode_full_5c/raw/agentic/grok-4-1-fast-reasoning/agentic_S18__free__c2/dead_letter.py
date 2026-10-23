from typing import Dict
from messaging_client import publish_message, dead_letter_topic_id, get_topic_path
from messaging_models import PubSubMessage


def send_to_dead_letter(msg: PubSubMessage, error_msg: str) -> str:
    attributes = dict(msg.attributes)
    attributes["original_message_id"] = msg.message_id
    attributes["error"] = error_msg
    return publish_message(dead_letter_topic_id, msg.data, attributes)
