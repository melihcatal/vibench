import os
from google.cloud import translate_v3 as translate

from speech_models import TranslationResult

# Google Cloud project ID from environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

def translate_caption_chunk(text: str, target_language: str, source_language: str = "en") -> TranslationResult:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{PROJECT_ID}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Can be "text/plain" or "text/html"
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslationResult(
        text=translated_text,
        source_language=source_language,
        target_language=target_language
    )
