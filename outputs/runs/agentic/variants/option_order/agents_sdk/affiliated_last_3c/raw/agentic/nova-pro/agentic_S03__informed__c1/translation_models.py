from translation_client import translate_client

def prepare_translation_request(text, target_language):
    return {'q': text, 'target': target_language}

def extract_translation_response(response):
    return response['translatedText']