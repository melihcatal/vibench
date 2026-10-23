from google.cloud import translate_v2 as translate
import os


def translate_log_message(text, target_language_code="es"):
    """Translates support-visible log messages for another locale using Google Cloud Translation.

    Args:
        text (str): The log message text to translate.
        target_language_code (str): The BCP-47 language code of the target language (e.g., 'es' for Spanish).

    Returns:
        dict: A dictionary containing the original text, translated text, and detected source language.
              Returns an error message if translation fails.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        # Google Cloud Translation automatically detects the source language
        result = client.translate(text, target_language=target_language_code)

        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "target_language": target_language_code,
        }
    except Exception as e:
        return {"error": f"Google Cloud Translation API failed: {e}"}


if __name__ == "__main__":
    # Example usage with log messages
    messages_to_translate = [
        "User authentication failed due to invalid credentials.",
        "La base de datos no responde.",  # Example in Spanish
        "Service worker registered successfully.",
    ]

    print("\n--- Translating Log Messages ---")
    for msg in messages_to_translate:
        # Translate to Spanish by default
        translation_result = translate_log_message(msg, target_language_code="es")
        print(f"Original: '{msg}'")
        print(f"Translation (es): {translation_result}")
        print("---")

        # Translate to French
        translation_result_fr = translate_log_message(msg, target_language_code="fr")
        print(f"Original: '{msg}'")
        print(f"Translation (fr): {translation_result_fr}")
        print("---")
