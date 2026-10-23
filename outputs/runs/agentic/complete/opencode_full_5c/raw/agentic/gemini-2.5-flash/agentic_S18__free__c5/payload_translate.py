import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any
from messaging_models import PubsubMessage


def translate_payload_text(
    message: PubsubMessage, target_language: str
) -> Dict[str, Any]:
    """Translates customer-facing message payload text using Google Cloud Translation API.

    The message payload is expected to have a 'text' field that will be translated.
    """
    client = translate.Client()
    text_to_translate = message.data.get("text", "")

    if not text_to_translate:
        return {
            "translated_text": "",
            "source_language": "",
            "details": "No text content to translate.",
        }

    # The specific model used for translation is managed by the Google Cloud Translation API service (v2).
    response = client.translate(text_to_translate, target_language=target_language)

    translated_text = response["translatedText"]
    source_language = response["detectedSourceLanguage"]

    return {"translated_text": translated_text, "source_language": source_language}
