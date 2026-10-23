from google.cloud import translate_v3 as translate

def translate_text(
    project_id: str,
    text: str,
    source_language_code: str,
    target_language_code: str,
) -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
