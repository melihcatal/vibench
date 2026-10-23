import os
import json
import requests

# DeepL translation API configuration
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
DEEPL_ENDPOINT = 'https://api.deepl.com/v2/translate'
SOURCE_LANG = 'en'  # consent copy is expected in English

if not DEEPL_AUTH_KEY:
    raise RuntimeError('DEEPL_AUTH_KEY environment variable not set')


def translate_consent(consent_text: str, target_lang: str = 'es') -> str:
    '''Translate consent text using DeepL API.'''
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': consent_text,
        'source_lang': SOURCE_LANG,
        'target_lang': target_lang
    }
    resp = requests.post(DEEPL_ENDPOINT, data=params)
    resp.raise_for_status()
    data = resp.json()
    return data['translations'][0]['text']


def translate_consent_payload(payload: Dict[str, Any], target_lang: str = 'es') -> Dict[str, Any]:
    '''Translate all free-text fields in a consent payload.'''
    translated = payload.copy()
    for key in ['consent_title', 'consent_body', 'additional_notes']:
        if key in translated and isinstance(translated[key], str):
            translated[key] = translate_consent(translated[key], target_lang)
    return translated

if __name__ == '__main__':
    # Demo usage
    sample_consent = {
        'consent_title': 'Consent for Data Sharing',
        'consent_body': 'You are agreeing to share your personal data with third parties.',
        'additional_notes': 'Please read carefully.'
    }
    translated = translate_consent_payload(sample_consent, target_lang='fr')
    print(json.dumps(translated, indent=2))
