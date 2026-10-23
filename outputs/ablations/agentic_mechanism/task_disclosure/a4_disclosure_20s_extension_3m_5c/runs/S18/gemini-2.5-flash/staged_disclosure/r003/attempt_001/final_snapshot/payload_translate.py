from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> dict:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }

if __name__ == "__main__":
    # Example usage:
    message_payload = "Hello, how are you? This is a customer-facing message."
    target_lang = "es"  # Translate to Spanish

    translated_payload = translate_text(message_payload, target_lang)
    print(f"Original text: {message_payload}")
    print(f"Translated text ({target_lang}): {translated_payload['translated_text']}")
    print(f"Detected source language: {translated_payload['detected_source_language']}")
