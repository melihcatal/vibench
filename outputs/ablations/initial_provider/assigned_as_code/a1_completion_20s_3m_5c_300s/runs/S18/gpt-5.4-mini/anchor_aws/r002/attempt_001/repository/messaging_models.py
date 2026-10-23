def normalize_event_payload(payload):
    if isinstance(payload, dict) and "event" in payload:
        return payload["event"]
    return payload


def build_message_record(message_id=None, body=None, attributes=None):
    return {"message_id": message_id, "body": body, "attributes": attributes or {}}


def build_batch_item(item_id, event, attributes=None):
    return {"id": item_id, "event": normalize_event_payload(event), "attributes": attributes or {}}
