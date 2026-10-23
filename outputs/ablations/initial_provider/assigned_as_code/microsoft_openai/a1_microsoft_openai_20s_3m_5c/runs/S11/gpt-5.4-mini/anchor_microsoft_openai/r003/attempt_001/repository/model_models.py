def normalize_platform_payload(payload):
    if isinstance(payload, str):
        return {'text': payload}
    return {'text': payload.get('text', '')}


def normalize_platform_response(response):
    if isinstance(response, dict):
        return response
    text = getattr(response, 'text', None)
    if text is not None:
        return {'text': text}
    return {'text': ''}
