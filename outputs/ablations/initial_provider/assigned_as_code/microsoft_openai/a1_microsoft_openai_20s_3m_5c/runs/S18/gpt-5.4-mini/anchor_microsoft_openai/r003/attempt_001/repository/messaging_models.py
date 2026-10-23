import json


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        return json.loads(payload)
    return payload


def normalize_message_body(message):
    body = getattr(message, 'body', message)
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    if isinstance(body, str):
        try:
            return json.loads(body)
        except Exception:
            return {'text': body}
    return body


def make_result(status, **fields):
    result = {'status': status}
    result.update(fields)
    return result
