import json
from typing import Any, Dict, Iterable, List, Optional

from messaging_client import get_sns_client, require_config
from messaging_models import normalize_payload, normalize_attributes, make_message_record


def batch_publish(messages: Iterable[Dict[str, Any]], topic_arn: Optional[str] = None) -> Dict[str, Any]:
    cfg = require_config()
    client = get_sns_client()
    records: List[Dict[str, Any]] = []
    for item in messages:
        payload = normalize_payload(item.get("payload"))
        attrs = normalize_attributes(item.get("attributes"))
        response = client.publish(
            TopicArn=topic_arn or cfg["topic_arn"],
            Message=json.dumps(payload, ensure_ascii=False),
            MessageAttributes=attrs,
        )
        records.append(make_message_record(
            provider="aws_sns",
            action="batch_publish",
            message_id=response.get("MessageId") or item.get("id"),
            status="sent",
            details={"response": response, "input_id": item.get("id")},
        ))
    return {"provider": "aws_sns", "count": len(records), "records": records}
