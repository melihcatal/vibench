import os
from google.cloud import translate_v3 as translate
from document_client import get_translate_client
from document_models import TranslatedTextResponse


def translate_ocr_text(
    text: str, target_language: str, source_language: str = None
) -> TranslatedTextResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_translate_client()

    parent = f"projects/{project_id}"

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": target_language,
            }
        )

    translated_text = ""
    detected_language = None
    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_language = response.translations[0].detected_language_code

    return TranslatedTextResponse(
        translated_text=translated_text, detected_language=detected_language
    )
