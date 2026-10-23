from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    project_id: str,
    target_language: str,
    source_language: str = None
) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project.
        target_language: The language to translate to (e.g., "fr" for French).
        source_language: The language of the input text (e.g., "en" for English).
                         If None, the API will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

    return response.translations[0].translated_text
