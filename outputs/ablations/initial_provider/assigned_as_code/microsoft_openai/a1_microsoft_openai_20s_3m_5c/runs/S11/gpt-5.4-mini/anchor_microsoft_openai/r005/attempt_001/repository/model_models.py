def normalize_text_response(response):
    text = ''
    if isinstance(response, dict):
        text = response.get('text', '') or ''
    return {'text': text}


def make_user_message(text):
    return {'role': 'user', 'content': text}


def collect_message_text(choice):
    return getattr(getattr(choice, 'message', None), 'content', '') or ''
