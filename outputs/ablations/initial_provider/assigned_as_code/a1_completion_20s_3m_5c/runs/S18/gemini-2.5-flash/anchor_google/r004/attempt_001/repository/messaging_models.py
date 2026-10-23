import json

def create_message_payload(event_data, attributes=None):
    if attributes is None:
        attributes = {}
    return {
        "data": json.dumps(event_data).encode("utf-8"),
        "attributes": attributes
    }

def parse_message_payload(message):
    data = json.loads(message.data.decode("utf-8"))
    attributes = dict(message.attributes)
    return {"data": data, "attributes": attributes, "message_id": message.message_id}
