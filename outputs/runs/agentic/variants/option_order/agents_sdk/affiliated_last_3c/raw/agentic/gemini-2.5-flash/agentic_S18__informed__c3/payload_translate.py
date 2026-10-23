import os
from google.cloud import translate_v2 as translate
from messaging_models import PubSubMessage

# Google Cloud Translation provider-specific signal

def translate_payload_text(message: PubSubMessage, target_language: str = "es") -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment for authentication
    translate_client = translate.Client()

    text_to_translate = str(message.data) # Assuming the message data can be converted to a string for translation

    # The target language for translation
    result = translate_client.translate(text_to_translate, target_language=target_language)

    return {
        "original_text": text_to_translate,
        "translated_text": result['translatedText'],
        "source_language": result['detectedSourceLanguage'],
        "target_language": target_language
    }
