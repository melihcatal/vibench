from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, source_language: str = None) -> dict:
    """Translates user-facing document fields using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English). If None,
                         Google Cloud Translation will attempt to detect the source language.

    Returns:
        A dictionary containing the translated text and detected source language.
        Example: {"translated_text": "Hola Mundo", "detected_source_language": "en"}
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
