from google.cloud import translate_v3 as translate

def batch_translate_text(
    texts: list[str],
    target_language_code: str,
    project_id: str
) -> list[str]:
    """Translates a list of strings into the target language while preserving order."""

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language_code,
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts
