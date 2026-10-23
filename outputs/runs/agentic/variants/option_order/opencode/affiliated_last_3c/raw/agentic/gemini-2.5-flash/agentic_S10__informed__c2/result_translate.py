import os
from google.cloud import translate


def translate_text(
    text: str, target_language: str, project_id: str, source_language: str = None
) -> dict:
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Detail on supported types can be found here: https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language,  # Optional. If omitted, language auto-detected.
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language_code = response.translations[0].detected_language_code

    return {
        "translated_text": translated_text,
        "detected_language_code": detected_language_code,
    }
