import os
import json
from typing import Dict, Any
import requests

# --------------------------------------------------------------
# Consent Translation Helper – fetches provider consent copy and translates it
# --------------------------------------------------------------

def load_translator_config() -> Dict[str, Any]:
    """Read a JSON config that maps language codes to translation API settings."""
    config_path = os.getenv('CONSULT_TRANSLATION_CONFIG', 'consent_translation_config.json')
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception:
        raise RuntimeError('Consent translation config not found or invalid')

TRANSLATOR_CONFIG = load_translator_config()

# Example translation API – Google Translate (replace with any provider)
TRANSLATE_ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'
API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY')
if not API_KEY:
    raise RuntimeError('GOOGLE_TRANSLATE_API_KEY must be set')


def translate_consent(source_text: str, target_lang: str = 'es') -> str:
    """Translate consent text using configured translation service."""
    payload = {
        'q': source_text,
        'target': target_lang,
        'format': 'text',
        'key': API_KEY,
    }
    resp = requests.post(TRANSLATE_ENDPOINT, data=payload)
    if resp.status_code != 200:
        raise Exception(f'Consent translation request failed: {resp.status_code} {resp.text}')
    result = resp.json()
    # Google Translate v2 returns data.translations[0].translatedText
    try:
        return result['data']['translations'][0]['translatedText']
    except KeyError:
        raise Exception(f'Unexpected translation response: {result}')


def fetch_provider_consent(scope: str) -> str:
    """Placeholder: retrieve the raw consent string from the IdP.
    In practice you would call the IdP's OAuth/ Consent screen endpoint or parse it from PKCE flow.
    For demo we return a static example string."
    return 'Consent to share your name, email, and profile picture with our application.'


def translate_consent_copy(scope: str, target_lang: str = 'es') -> Dict[str, Any]:
    raw = fetch_provider_consent(scope)
    translated = translate_consent(raw, target_lang)
    return {
        'scope': scope,
        'original': raw,
        'target_language': target_lang,
        'translated': translated,
    }
