from google.cloud import translate
import os


def translate_compliance_note(text: str, target_language: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()

    # The parent format is `projects/{project_id}/locations/{location}`.
    # For global resources, use `global` for the location.
    parent = f"projects/{project_id}/locations/global"

    # Translate the text using Google Cloud Translation.
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    # The translated text is in the first translation's `translated_text` attribute.
    return response.translations[0].translated_text
