def as_text(payload):
    if payload is None:
        return ''
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ('text', 'content', 'input', 'prompt', 'question', 'context'):
            value = payload.get(key)
            if isinstance(value, str):
                return value
    return str(payload)


def normalize_result_text(text):
    return {'text': text or ''}


def normalize_json_result(data):
    return {'json': data}
