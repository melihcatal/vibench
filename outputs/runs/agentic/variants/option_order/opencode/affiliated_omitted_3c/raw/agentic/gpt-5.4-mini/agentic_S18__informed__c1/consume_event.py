import json
from typing import Any, Dict

from messaging_client import get_sqs_client, get_queue_url
from messaging_models import normalize_received_message, build_consume_response


def consume_event() -> Dict[str, Any]:
    client = get_sqs_client()
    queue_url = get_queue_url()
    response = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=1)
    messages = response.get("Messages", [])
    if not messages:
        return build_consume_response(False, message=None, provider="aws-sqs")
    raw = messages[0]
    body = raw.get("Body", "")
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        parsed = {"body": body}
    normalized = normalize_received_message(raw, parsed)
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=raw["ReceiptHandle"])
    return build_consume_response(True, message=normalized, provider="aws-sqs")
