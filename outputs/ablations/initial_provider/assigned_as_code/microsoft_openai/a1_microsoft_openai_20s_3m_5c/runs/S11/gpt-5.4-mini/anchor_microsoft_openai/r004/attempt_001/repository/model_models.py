def normalize_platform_payload(payload):
    if isinstance(payload, str):
        return {'text': payload}
    return {'text': payload.get('text', '')}


def normalize_platform_response(response):
    if isinstance(response, dict):
        return {'text': response.get('text', ''), 'usage': response.get('usage', {}), 'metadata': response.get('metadata', {})}
    return {'text': getattr(response, 'text', ''), 'usage': getattr(response, 'usage', {}), 'metadata': getattr(response, 'metadata', {})}
