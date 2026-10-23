import os
from google.cloud import translate_v3 as translate

def translate_consent_copy(text: str, target_language: str, project_id: str, source_language: str = "en") -> str:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    # The Google Cloud Translation API returns a list of translations.
    if response.translations:
        return response.translations[0].translated_text
    return ""
