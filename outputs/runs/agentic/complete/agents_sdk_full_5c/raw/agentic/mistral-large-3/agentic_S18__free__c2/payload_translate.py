import os
from google.cloud import translate_v2 as translate
from messaging_models import ProcessedMessage

client = translate.Client()
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "es")

def translate_payload(processed_message: ProcessedMessage) -> dict:
    translated_payload = {}
    for key, value in processed_message.payload.items():
        if isinstance(value, str):
            result = client.translate(value, target_language=TARGET_LANGUAGE)
            translated_payload[key] = result["translatedText"]
        else:
            translated_payload[key] = value
    
    return translated_payload