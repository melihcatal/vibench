import json
from typing import Any, Dict, Optional

from messaging_client import get_sqs_client, require_config
from messaging_models import normalize_payload, make_message_record


def dead_letter(payload: Any, queue_url: Optional[str] = None, reason: Optional[str] = None) -> Dict[str, Any]:
    cfg = require_config()
    client = get_sqs_client()
    body = normalize_payload(payload)
    message_body = json.dumps({"reason": reason, "payload": body}, ensure_ascii=False)
    response = client.send_message(
        QueueUrl=queue_url or cfg["dead_letter_queue_url"],
        MessageBody=message_body,
    )
    return make_message_record(
        provider="aws_sqs",
        action="dead_letter",
        message_id=response.get("MessageId"),
        status="sent",
        details=response,
    )
