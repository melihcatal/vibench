import os
from google.cloud import translate_v2 as translate

def translate_payload(payload: dict, target_lang: str = 'es') -> dict:
    """Translate any 'text' field inside payload to the target language."""
    if 'text' not in payload:
        return payload  # nothing to translate
    client = translate.Client()  # picks up GOOGLE_APPLICATION_CREDENTIALS automatically
    original = payload['text']
    result = client.translate(original, target_language=target_lang)
    payload['translated_text'] = result['translatedText']
    payload['detected_source'] = result.get('detectedSourceLanguage')
    return payload

# Example usage (requires GOOGLE_APPLICATION_CREDENTIALS set to a service account with translate permission)
if __name__ == '__main__':
    p = {'text': 'Hello, world!', 'id': 'msg-1'}
    print('Translated payload:', translate_payload(p, target_lang='fr'))
