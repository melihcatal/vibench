# payload_translate.py
# [LATER-STEP]
# Translate customer‑facing text in a Pub/Sub message using Google Cloud Translation.

import os
from google.cloud import translate_v2 as translate
from .messaging_models import EventPayload

def translate_payload(payload: EventPayload, target_language: str = 'es') -> EventPayload:
    """Translate the 'text' field of the payload to the specified target language.

    Returns a new EventPayload with updated text. Non‑string payloads are left unchanged.
    """
    text = payload.data.get('text')
    if not isinstance(text, str):
        # Nothing to translate
        return payload
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    # Replace the original text with translation while preserving other fields
    new_data = payload.data.copy()
    new_data['text'] = result['translatedText']
    return EventPayload(data=new_data)
