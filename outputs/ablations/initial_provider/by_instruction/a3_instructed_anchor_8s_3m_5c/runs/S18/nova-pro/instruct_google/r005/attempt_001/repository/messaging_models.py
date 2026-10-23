import json

def normalize_message(message):
    return json.loads(message)

def serialize_message(message):
    return json.dumps(message).encode('utf-8')