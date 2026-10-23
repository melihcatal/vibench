import json


def normalize_response(response):
    return json.loads(response["body"].read())
