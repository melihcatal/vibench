import os
from google.cloud import translate_v3 as translate
from typing import Dict, Any

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

def translate_platform_output(text: str, target_language_code: str, source_language_code: str = None) -> Dict[str, Any]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global" # Translation API typically uses 'global' for most services
    parent = f"projects/{PROJECT_ID}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code, # Optional
            "mime_type": "text/plain",
        }
    )

    translated_text = ""
    detected_source_language = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return {
        "translated_text": translated_text,
        "target_language_code": target_language_code,
        "detected_source_language": detected_source_language,
        "raw_response": response.translations # Include raw response objects for debugging/metadata
    }