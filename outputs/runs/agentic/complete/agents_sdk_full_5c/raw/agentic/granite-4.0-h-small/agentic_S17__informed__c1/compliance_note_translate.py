import json
import os
import requests
from security_models import ResponseEnvelope

def translate_note(note: str, target_lang: str = 'es') -> str:
    """Translate an encryption/compliance note for reviewers.

    Uses DeepL API to translate from source language (default 'en') to target language.
    Returns the translated text.
    
    Args:
        note (str): Original note in English.
        target_lang (str): ISO language code for target language (default 'es' for Spanish).
    
    Returns:
        str: Translated note.
    """
    deepl_auth = os.getenv('DEEPL_AUTH_KEY')
    if not deepl_auth:
        raise RuntimeError('DEEPL_AUTH_KEY environment variable not set')
    url = 'https://api.deepl.com/v2/translate'
    params = {
        'auth_key': deepl_auth,
        'text': note,
        'target_lang': target_lang
    }
    resp = requests.post(url, data=params)
    resp.raise_for_status()
    data = resp.json()
    return data['translations'][0]['text']


def translate_response(response: ResponseEnvelope) -> ResponseEnvelope:
    """Translate audit messages inside a ResponseEnvelope.

    Currently the envelope may contain optional fields `ciphertext`, `plaintext`, etc.
    This stub demonstrates adding a `compliance_note` field, translating it, and returning
    an updated envelope.
    """
    # Example: add a compliance note
    original_note = 'The plaintext was encrypted using an AES-256-GCM envelope with an RSA-2048 signing key.'
    translated_note = translate_note(original_note)
    # Append the translated note to the envelope (as an extra attribute for downstream consumers)
    new_dict = response.to_dict()
    new_dict['compliance_note_translated'] = translated_note
    return ResponseEnvelope.from_dict(new_dict)
