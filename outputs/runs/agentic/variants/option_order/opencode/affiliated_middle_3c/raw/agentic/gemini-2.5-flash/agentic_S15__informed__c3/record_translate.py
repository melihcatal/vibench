import os
from google.cloud import translate_v2 as translate


def translate_record_text(text: str, target_language: str = "es") -> dict:
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # The client creation `translate.Client()` identifies the provider.
    # No explicit GOOGLE_APPLICATION_CREDENTIALS check needed, as the SDK handles it implicitly via environment variables or gcloud cli.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return {
        "input_text": text,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
