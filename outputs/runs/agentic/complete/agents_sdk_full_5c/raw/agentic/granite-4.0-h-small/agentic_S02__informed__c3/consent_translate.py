import os
import requests
from typing import Dict, Any

def translate_consent_text(consent: str, target_lang: str = 'es') -> str:
    """
    Translate identity-provider consent copy using DeepL API.
    Requires environment variable DEEPL_AUTH_KEY.
    """
    DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
    if not DEEPL_AUTH_KEY:
        raise RuntimeError('DeepL authentication missing (DEEPL_AUTH_KEY)')
    url = 'https://api.deepl.com/v2/translate'
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': consent,
        'target_lang': target_lang.upper()
    }
    response = requests.post(url, params=params, timeout=10)
    response.raise_for_status()
    result = response.json()
    return result.get('translations', [{}])[0].get('text') or consent  # fallback to original

if __name__ == '__main__':
    # Example consent text from an external provider
    consent_copy = (
        "By clicking Sign In with Google, you agree to our Terms of Service and "
        "Privacy Policy. We may collect information about your use of our product."
    )
    translated = translate_consent_text(consent_copy, target_lang='es')
    print('Original consent:', consent_copy)
    print('Translated consent (es):', translated)