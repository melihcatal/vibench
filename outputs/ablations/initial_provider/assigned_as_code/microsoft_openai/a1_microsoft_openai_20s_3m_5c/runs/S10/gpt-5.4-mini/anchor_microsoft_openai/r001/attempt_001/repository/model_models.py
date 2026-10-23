def text_from_payload(payload, key='text'):
    return '' if payload is None else str(payload.get(key, ''))


def normalize_text(value):
    return '' if value is None else str(value)


def extract_message_content(response):
    return response.choices[0].message.content or ''


def extract_stream_content(chunk):
    choices = getattr(chunk, 'choices', [])
    if not choices:
        return ''
    delta = getattr(choices[0], 'delta', None)
    return '' if delta is None else getattr(delta, 'content', '') or ''
