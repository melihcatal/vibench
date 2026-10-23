from google.cloud import translate_v3 as translate
import os


def translate_text(
    text: str,
    project_id: str,
    target_language_code: str,
    source_language_code: str = None,
) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
    )
    return response.translations[0].translated_text
