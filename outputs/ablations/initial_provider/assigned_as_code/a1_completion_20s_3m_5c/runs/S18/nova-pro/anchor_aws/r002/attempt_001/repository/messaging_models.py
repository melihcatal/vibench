import json


def normalize_payload(payload):
    return json.loads(json.dumps(payload))