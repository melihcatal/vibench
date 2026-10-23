def normalize_text_response(response):
    if isinstance(response, dict):
        return {'text': response.get('text', ''), 'metadata': response.get('metadata', {})}
    text = getattr(response, 'text', '') or ''
    metadata = getattr(response, 'metadata', {}) or {}
    return {'text': text, 'metadata': metadata}


def build_prompt(text, locale=None):
    prompt = {'text': text}
    if locale:
        prompt['locale'] = locale
    return prompt
