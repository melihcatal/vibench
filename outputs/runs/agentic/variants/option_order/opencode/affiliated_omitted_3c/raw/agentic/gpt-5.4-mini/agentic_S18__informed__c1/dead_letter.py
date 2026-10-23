import json
from typing import Any, Dict

from messaging_client import get_sns_client, get_dead_letter_topic_arn
from messaging_models import normalize_message_payload, build_dead_letter_response


def send_dead_letter(payload: Dict[str, Any], reason: str) -> Dict[str, Any]:
    client = get_sns_client()
    topic_arn = get_dead_letter_topic_arn()
    normalized = normalize_message_payload(payload)
    message = json.dumps({"reason": reason, "payload": normalized}, separators=(",", ":"), sort_keys=True)
    response = client.publish(TopicArn=topic_arn, Message=message, Subject="dead-letter")
    return build_dead_letter_response(True, message_id=response.get("MessageId"), provider="aws-sns")
