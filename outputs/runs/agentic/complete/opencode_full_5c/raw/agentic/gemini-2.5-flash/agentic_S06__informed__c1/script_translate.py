import os
from google.cloud import translate_v3 as translate


def translate_text(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = None,
):
    """Translates text into the target language.

    Args:
        project_id: The ID of the GCP project.
        text: The text to translate.
        target_language_code: The language to translate the text into.
        source_language_code: The language of the text. If not specified,
                               the API will attempt to detect the language.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts[0] if translated_texts else None
