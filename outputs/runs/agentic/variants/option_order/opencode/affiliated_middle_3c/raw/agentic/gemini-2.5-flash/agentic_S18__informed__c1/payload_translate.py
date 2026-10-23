import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation provider-identifying signal: google.cloud.translate_v2


def translate_payload_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """Translates customer-facing message payload text using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment or configured via gcloud auth
    # No explicit API key needed if credentials are set up for the environment.

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    # The translated text is in 'translatedText'
    translated_text = result["translatedText"]
    return translated_text
