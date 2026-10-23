import json

def serialize_message(message):
    return json.dumps(message).encode('utf-8')

def deserialize_message(data):
    return json.loads(data.decode('utf-8'))