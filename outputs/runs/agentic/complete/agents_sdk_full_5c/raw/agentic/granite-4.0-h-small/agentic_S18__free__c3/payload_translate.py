import json
from typing import Dict, Any
from google.cloud import translate_v2 as translate
from messaging_models import MessagePayload

# Translate client - uses Application Default Credentials or explicit credentials file
translate_client = translate.Client()
TARGET_LANGUAGE = 'es'  # example target language code, adjust as needed


def translate_payload(event: Dict[str, Any]) -> MessagePayload:
    """Translate the textual content in a payload and return a new MessagePayload.

    Expects the payload to have a 'message' field under the 'data' dict.
    """
    raw = MessagePayload(**event)
    original = raw.data.get('message', '')
    if not original:
        print(f"No 'message' field in payload {raw.event_id}; skipping translation.")
        return raw
    # Call Google Cloud Translation API
    response = translate_client.translate(original, target_language=TARGET_LANGUAGE)
    translated_text = response['translatedText']
    # Build a new payload with translated text and a translation metadata flag
    translated_payload = raw.copy(update={
        'data': {**raw.data, 'message': translated_text, 'translation': {
            'target': TARGET_LANGUAGE,
            'source': response.get('detectedSourceLanguage'),
            'raw': original
        }}
    })
    print(f"Translated {original} -> {translated_text} for event {translated_payload.event_id}")
    return translated_payload

# Simple test when run directly
if __name__ == '__main__':
    sample = {
        'event_id': 'demo-trans-001',
        'timestamp': '2025-08-14T12:00:00Z',
        'data': {'message': 'Hello, world!'}
    }
    translated = translate_payload(sample)
    print('Translated payload:', json.dumps(translated.dict(), indent=2))
