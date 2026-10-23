from google.cloud import translate_v2 as translate
import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
client = translate.Client()


def translate_consent(text, target_language):
    result = client.translate(
        text,
        target_language=target_language
    )
    return {
        "translated_text": result['translatedText'],
        "detected_source_language": result['detectedSourceLanguage'],
        "provider": "google_translate"
    }