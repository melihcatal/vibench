import os
from google.cloud import translate_v3 as translate
from speech_models import TranslationResponse


def translate_live_caption(
    text: str,
    target_language_code: str = "fr",
) -> TranslationResponse | None:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        translation = response.translations[0]
        return TranslationResponse(
            translated_text=translation.translated_text,
            detected_language_code=translation.detected_language_code,
        )
    return None
