def coerce_message_payload(payload, raw_message=None):
    payload = payload if isinstance(payload, dict) else {"event": payload}
    event = payload.get("event", payload)
    return {
        "event": event,
        "message_id": (raw_message or {}).get("MessageId"),
        "receipt_handle": (raw_message or {}).get("ReceiptHandle"),
        "attributes": (raw_message or {}).get("MessageAttributes", {}),
    }


def coerce_message_records(payload):
    records = payload if isinstance(payload, list) else payload.get("records", []) if isinstance(payload, dict) else []
    normalized = []
    for index, record in enumerate(records):
        item = record if isinstance(record, dict) else {"event": record}
        normalized.append(
            {
                "id": item.get("id") or str(index),
                "event": item.get("event", item),
                "attributes": item.get("attributes", {}),
            }
        )
    return normalized
