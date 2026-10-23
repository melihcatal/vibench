def extract_text(response):
    return response.choices[0].message.content or ''


def normalize_json_text(text):
    return text.strip()


def wrap_text_result(text):
    return {'text': text or ''}


def wrap_json_result(text):
    return {'json': text or ''}
