from google.cloud import translate_v2 as translate
import os


def translate_script(text: str, target_language: str, source_language: str = None):
    client = translate.Client()
    
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return {
        'translated_text': result['translatedText'],
        'source_language': result['detectedSourceLanguage'],
        'target_language': target_language
    }
