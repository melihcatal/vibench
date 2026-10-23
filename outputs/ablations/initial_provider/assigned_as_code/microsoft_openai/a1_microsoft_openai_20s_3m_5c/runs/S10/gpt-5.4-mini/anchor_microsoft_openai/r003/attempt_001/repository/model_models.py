import json


def text_payload(text):
    return {'text': text}


def json_payload(text, schema=None):
    payload = {'text': text}
    if schema is not None:
        payload['schema'] = schema
    return payload


def normalize_text(response):
    return {'text': response or ''}


def normalize_json(text):
    if isinstance(text, dict):
        return text
    return json.loads(text)
