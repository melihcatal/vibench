import json


def normalize_payload(payload):
    return {"text": payload["text"]}


def parse_response(response):
    return json.loads(response)