import os
from google.cloud import translate

def translate_text(
    text: str,
    target_language_code: str,
    project_id: str,
    location: str = "global",
    source_language_code: str = "",
) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text into.
        project_id: The ID of the Google Cloud project.
        location: The location of the translation service. Defaults to "global".
        source_language_code: The language code of the input text. If not specified,
                              the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    # If source_language_code is empty, let the API detect it.
    if source_language_code:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )
    else:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language_code,
        )

    translated_text = response.translations[0].translated_text
    return translated_text