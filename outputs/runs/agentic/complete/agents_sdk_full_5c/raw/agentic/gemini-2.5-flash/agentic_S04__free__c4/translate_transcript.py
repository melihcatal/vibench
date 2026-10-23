from google.cloud import translate_v3 as translate

def translate_text_segments(project_id: str, text_segments: list[str], target_language: str = "es"):
    """
    Translates completed transcript segments using Google Cloud Translation.

    Args:
        project_id: Your Google Cloud project ID.
        text_segments: A list of text strings to translate.
        target_language: The target language code (e.g., "es" for Spanish).

    Returns:
        A list of translated text strings.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=text_segments,
        target_language_code=target_language,
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    print(f"Translated {len(text_segments)} segments to {target_language}.")
    return translated_texts
