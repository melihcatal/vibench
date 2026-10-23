from google.cloud import translate_v3 as translate

def batch_translate_strings(
    strings: list[str],
    project_id: str,
    source_language: str,
    target_language: str,
) -> list[str]:
    """Translates a list of strings using the Google Cloud Translation API,
    preserving the order of the input strings.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=strings,
        source_language_code=source_language,
        target_language_code=target_language,
        mime_type="text/plain",
    )

    translated_strings = [translation.translated_text for translation in response.translations]
    return translated_strings
