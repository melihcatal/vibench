def normalize_text_response(response):
    if isinstance(response, dict):
        return {'text': response.get('text', ''), 'metadata': response.get('metadata', {})}
    return {'text': getattr(response, 'text', '') or '', 'metadata': getattr(response, 'metadata', {}) or {}}


def build_user_payload(text):
    return {'text': text}
