import json

def serialize_payload(data):
    # Basic serialization for consistency
    return json.dumps(data).encode('utf-8')

def deserialize_payload(data):
    # Basic deserialization for consistency
    return json.loads(data.decode('utf-8'))
