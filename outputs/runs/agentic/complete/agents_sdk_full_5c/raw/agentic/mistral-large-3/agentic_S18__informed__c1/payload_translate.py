import os
from google.cloud import translate_v2 as translate
from messaging_models import EventMessage

client = translate.Client()

def translate_payload(event: EventMessage, target_language: str = "en") -> EventMessage:
    translated_payload = {}
    
    for key, value in event.payload.items():
        if isinstance(value, str):
            result = client.translate(value, target_language=target_language)
            translated_payload[key] = result["translatedText"]
        else:
            translated_payload[key] = value
    
    return EventMessage(
        event_id=event.event_id,
        payload=translated_payload,
        attributes=event.attributes
    )