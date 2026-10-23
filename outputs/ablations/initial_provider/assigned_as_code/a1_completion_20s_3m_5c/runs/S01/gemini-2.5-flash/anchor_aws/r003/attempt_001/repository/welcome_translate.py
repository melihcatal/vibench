import os
from google.cloud import translate_v2 as translate
from identity_models import TranslatedContent

def welcome_translate(payload, config=None) -> TranslatedContent:
    config = config or {}
    # Google Cloud credentials will be loaded automatically from the environment
    # if GOOGLE_APPLICATION_CREDENTIALS is set.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.
    translate_client = translate.Client()

    text_to_translate = payload["text"]
    target_language = payload["target_language"]

    response = translate_client.translate(
        text_to_translate, 
        target_language=target_language
    )

    translated_text = response["translatedText"]
    original_text = response["input"]

    return TranslatedContent(
        original_text=original_text,
        translated_text=translated_text,
        target_language=target_language
    )
