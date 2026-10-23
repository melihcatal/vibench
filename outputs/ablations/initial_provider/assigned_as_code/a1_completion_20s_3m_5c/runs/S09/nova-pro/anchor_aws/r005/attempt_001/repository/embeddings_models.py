import json


def normalize_request(payload):
    return json.dumps(payload)


def parse_response(response):
    return json.loads(response["body"].read())