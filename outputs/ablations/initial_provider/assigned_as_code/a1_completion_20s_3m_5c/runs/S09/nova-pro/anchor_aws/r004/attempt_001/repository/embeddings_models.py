import json


def normalize_payload(payload):
    return {"inputText": payload["text"]}


def parse_response(response):
    return json.loads(response["body"].read())["embedding"]