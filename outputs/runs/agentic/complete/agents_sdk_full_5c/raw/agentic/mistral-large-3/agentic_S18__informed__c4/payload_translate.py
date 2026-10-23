import os
from google.cloud import translate_v2 as translate
from messaging_models import EventMessage

client = translate.Client()

def translate_payload(event: EventMessage, target_language: str) -> EventMessage:
    result = client.translate(event.data, target_language=target_language)
    translated_event = EventMessage(
        data=result["translatedText"],
        attributes=event.attributes.copy(),
        message_id=event.message_id
    )
    return translated_event