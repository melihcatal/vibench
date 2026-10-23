from google.cloud import translate

def translate_transcript_segments(segments: list[str], target_language: str) -> list[str]:
    """
    Translates a list of transcript segments to a specified target language using Google Cloud Translation.

    Args:
        segments: A list of strings, where each string is a transcript segment.
        target_language: The language code to translate the segments into (e.g., "es" for Spanish).

    Returns:
        A list of translated strings.
    """
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    parent = f"projects/{project_id}/locations/global"

    translated_segments = []
    for segment in segments:
        response = client.translate_text(
            parent=parent,
            contents=[segment],
            target_language_code=target_language,
        )
        for translation in response.translations:
            translated_segments.append(translation.translated_text)
    return translated_segments
