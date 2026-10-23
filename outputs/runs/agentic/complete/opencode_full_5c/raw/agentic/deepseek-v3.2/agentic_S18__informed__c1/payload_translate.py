import os
from google.cloud import translate_v2 as translate


def translate_message_payload(text, target_language="en", source_language=None):
    """Translate customer-facing message payload text using Google Cloud Translation."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result.get(
            "detectedSourceLanguage", source_language
        ),
        "target_language": target_language,
        "model": "google-cloud-translation-v2",
    }
