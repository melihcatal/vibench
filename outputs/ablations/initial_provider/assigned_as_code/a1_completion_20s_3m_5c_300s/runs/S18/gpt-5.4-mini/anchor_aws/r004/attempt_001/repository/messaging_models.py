import json
from datetime import datetime, timezone


def normalize_message(payload):
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {"event": payload}
    if payload is None:
        payload = {}
    if "timestamp" not in payload:
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    return payload


def build_batch_entry(message, index):
    message = normalize_message(message)
    message_id = message.get("id") or message.get("message_id") or f"message-{index}"
    return {
        "Id": str(message_id),
        "Message": json.dumps(message),
        "MessageAttributes": {k: {"DataType": "String", "StringValue": str(v)} for k, v in message.get("attributes", {}).items()},
    }


def parse_sns_publish_response(response):
    return {"message_id": response.get("MessageId")}


def parse_sqs_message(message):
    body = message.get("Body")
    try:
        body = json.loads(body)
    except Exception:
        pass
    return {"message_id": message.get("MessageId"), "receipt_handle": message.get("ReceiptHandle"), "body": body}
