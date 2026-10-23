import os
import json
from google.cloud import translate_v2 as translate

def translate_payload(message: Dict[str, any], target_lang: str = 'es') -> Dict[str, any]:
    """Translate the text field inside a message payload.
    Uses Google Cloud Translation API.
    """
    # Ensure required env var for credentials is set (application default or explicit)
    client = translate.Client()
    payload = message.get('payload', '')
    if isinstance(payload, str):
        translation = client.translate(payload, target_language=target_lang)['translatedText']
        # Return a new dict with translated text
        return {'payload': translation, 'original': payload, 'target_lang': target_lang}
    return message  # if no string payload, return unchanged
