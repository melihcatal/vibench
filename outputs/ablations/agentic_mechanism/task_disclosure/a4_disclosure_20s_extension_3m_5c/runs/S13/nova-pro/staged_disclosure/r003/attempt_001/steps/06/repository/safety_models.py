def create_text_content_safety_request(text):
    return {
        'text': text,
    }


def create_text_content_safety_response(response):
    return {
        'safe': response.get('safe', False),
        'reason': response.get('reason', '')
    }


def normalize_text_content_safety_response(response):
    return {
        'safe': response['safe'],
        'reason': response['reason'].lower()
    }