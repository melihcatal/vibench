import os
import requests
from google.cloud import translate_v2 as translate
from messaging_models import normalize_message

# Preferred cloud translation service; here using Google Cloud Translation.
# You can switch implementation based on env var TRANSLATOR_SERVICE.
TRANSLATOR_SERVICE = os.getenv('TRANSLATOR_SERVICE', 'google')

if TRANSLATOR_SERVICE == 'google':
    # Google Cloud Translation client library
    def translate_payload(text: str, target_lang: str) -> str:
        """Translate text using Google Cloud Translation."""
        client = translate.Client()
        result = client.translate(text, target_language=target_lang)
        return result['translatedText']
else:
    # Placeholder for other providers (e.g., Azure, AWS, Alibaba)
    def translate_payload(text: str, target_lang: str) -> str:
        raise NotImplementedError(f"Translation service {TRANSLATOR_SERVICE} not implemented")


def translate_message(msg: dict, target_lang: str) -> dict:
    """Translate the 'text' field of a message payload.

    Returns a new dict with the translated text replacing the original.
    """
    original = msg.get('text')
    if not original:
        return msg  # Nothing to translate
    translated = translate_payload(original, target_lang)
    new_msg = normalize_message(msg.copy())
    new_msg['text'] = translated
    return new_msg
