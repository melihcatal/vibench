from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, project_id: str, source_language: str = "en") -> dict:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "fr" for French).
        project_id: The Google Cloud project ID.
        source_language: The language of the input text (defaults to "en").

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language, source_language=source_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
