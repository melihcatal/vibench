import json


def normalize_payload(payload):
    return {"text": payload['text']}


def normalize_response(response):
    return {"embedding": response['embedding']}