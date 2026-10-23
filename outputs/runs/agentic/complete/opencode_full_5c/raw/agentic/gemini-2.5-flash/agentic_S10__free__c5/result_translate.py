import os
from google.cloud import translate_v3 as translate
from model_models import LLMResponse


def translate_model_output(
    text: str,
    target_language_code: str,
    project_id: str = os.environ.get("GOOGLE_CLOUD_PROJECT"),
) -> LLMResponse:
    """
    Translates generated model output using Google Cloud Translation API.
    """
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable not set for translation."
        )

    client = translate.TranslationServiceClient()
    location = "global"  # Translation API is global for most regions.

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            # "source_language_code": "en", # Optional, can be auto-detected
            "mime_type": "text/plain",
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return LLMResponse(
        text=translated_text,
        metadata={
            "translation_provider": "google_cloud_translation",
            "target_language": target_language_code,
        },
    )
