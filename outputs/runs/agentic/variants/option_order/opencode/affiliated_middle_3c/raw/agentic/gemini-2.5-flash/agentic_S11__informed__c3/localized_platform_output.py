from google.cloud import translate_v3 as translate
import os
from model_models import TranslationResult


def translate_platform_output(
    text: str, target_language: str, project_id: str
) -> TranslationResult:
    client = translate.TranslationServiceClient()
    location = "global"  # Or your specific region
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    translated_text = ""
    detected_source_language = ""

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return TranslationResult(
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )
