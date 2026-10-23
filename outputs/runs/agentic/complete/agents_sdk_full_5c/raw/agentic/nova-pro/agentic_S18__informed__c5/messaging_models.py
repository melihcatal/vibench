import json

def normalize_payload(payload):
    return json.dumps(payload).encode('utf-8')

def parse_response(response):
    return json.loads(response.data)