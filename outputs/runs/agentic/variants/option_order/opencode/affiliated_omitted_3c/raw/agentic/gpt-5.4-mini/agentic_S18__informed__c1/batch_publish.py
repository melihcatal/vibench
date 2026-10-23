import json
from typing import Any, Dict, Iterable, List

from messaging_client import get_sns_client, get_topic_arn
from messaging_models import normalize_message_payload, build_batch_publish_response


def batch_publish(messages: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = get_sns_client()
    topic_arn = get_topic_arn()
    entries: List[Dict[str, Any]] = []
    for index, payload in enumerate(messages):
        normalized = normalize_message_payload(payload)
        entries.append({
            "Id": str(normalized.get("id", index)),
            "Message": json.dumps(normalized, separators=(",", ":"), sort_keys=True),
        })
    results = []
    for entry in entries:
        response = client.publish(TopicArn=topic_arn, Message=entry["Message"], Subject=entry["Id"][:100])
        results.append({"id": entry["Id"], "message_id": response.get("MessageId")})
    return build_batch_publish_response(True, results=results, provider="aws-sns")
