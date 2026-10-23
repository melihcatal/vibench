from google.cloud import translate_v3 as translate

def translate_segments(segments: list[str], target_language: str) -> list[str]:
    """
    Translates a list of transcript segments to a specified target language using Google Cloud Translation.

    Args:
        segments: A list of strings, where each string is a transcript segment.
        target_language: The target language code (e.g., "es" for Spanish, "fr" for French).

    Returns:
        A list of translated strings, corresponding to the input segments.
    """
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    parent = f"projects/{project_id}/locations/global"

    translated_texts = []
    for segment in segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [segment],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts
