import json


def normalize_payload(payload):
    return json.dumps(payload)


def parse_response(response):
    return json.loads(response)