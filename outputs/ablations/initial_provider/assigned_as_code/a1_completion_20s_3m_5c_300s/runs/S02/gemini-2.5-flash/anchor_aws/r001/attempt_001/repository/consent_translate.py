import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text, target_language="en", source_language=None):
    # GOOGLE_APPLICATION_CREDENTIALS should be set as an environment variable
    # pointing to the service account key file.
    # Alternatively, you can explicitly pass credentials or use default client behavior
    # if running in a Google Cloud environment.

    translate_client = translate.Client()

    try:
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        translation_result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        return {
            "original_text": text,
            "translated_text": translation_result["translatedText"],
            "source_language": translation_result["detectedSourceLanguage"]
        }
    except Exception as e:
        return {"error": str(e)}
