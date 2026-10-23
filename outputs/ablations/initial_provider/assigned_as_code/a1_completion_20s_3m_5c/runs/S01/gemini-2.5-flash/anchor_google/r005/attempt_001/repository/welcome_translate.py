from google.cloud import translate_v2 as translate
import os
from identity_models import TranslatePayload

def welcome_translate(payload: TranslatePayload):
    client = translate.Client()
    
    # Text can also be a list of strings to translate.
    # For a single string, input is a string.
    result = client.translate(
        payload.text,
        target_language=payload.target_language,
        source_language=payload.source_language
    )
    
    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"]
    }
