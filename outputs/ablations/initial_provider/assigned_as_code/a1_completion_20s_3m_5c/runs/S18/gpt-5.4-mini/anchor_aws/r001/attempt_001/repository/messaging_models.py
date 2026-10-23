def normalize_message(payload):
    if isinstance(payload, dict):
        body = payload.get("body", payload.get("event", payload))
        message_id = payload.get("id") or payload.get("message_id")
        attributes = payload.get("attributes", {})
        return {"body": body, "message_id": message_id, "attributes": attributes}
    return {"body": payload, "message_id": None, "attributes": {}}


def normalize_result(response):
    if isinstance(response, dict):
        return {"message_id": response.get("message_id") or response.get("MessageId"), "raw": response}
    return {"message_id": None, "raw": response}
