import json


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {'text': payload}
    return dict(payload)


def build_event_message(payload, message_id=None, attributes=None):
    data = normalize_payload(payload)
    message = {'event': data}
    if message_id is not None:
        message['message_id'] = message_id
    if attributes:
        message['attributes'] = dict(attributes)
    return message


def parse_message_body(body):
    if body is None:
        return {}
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {'text': body}
    return dict(body)


def response_payload(status, **fields):
    payload = {'status': status}
    payload.update(fields)
    return payload
