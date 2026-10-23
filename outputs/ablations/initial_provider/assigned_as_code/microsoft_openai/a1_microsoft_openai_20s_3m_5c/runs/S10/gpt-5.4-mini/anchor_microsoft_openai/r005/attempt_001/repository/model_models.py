def normalize_text(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    return str(value)


def get_input_text(payload):
    if 'text' in payload:
        return normalize_text(payload['text'])
    if 'input' in payload:
        return normalize_text(payload['input'])
    return ''


def get_context(payload):
    return normalize_text(payload.get('context', ''))


def get_question(payload):
    return normalize_text(payload.get('question', ''))


def get_json_schema(payload):
    return payload.get('schema') or payload.get('json_schema') or {}


def response_text(response):
    return response.choices[0].message.content or ''


def streamed_text(chunks):
    parts = []
    for chunk in chunks:
        for choice in getattr(chunk, 'choices', []) or []:
            delta = getattr(choice, 'delta', None)
            if delta and getattr(delta, 'content', None):
                parts.append(delta.content)
    return ''.join(parts)
