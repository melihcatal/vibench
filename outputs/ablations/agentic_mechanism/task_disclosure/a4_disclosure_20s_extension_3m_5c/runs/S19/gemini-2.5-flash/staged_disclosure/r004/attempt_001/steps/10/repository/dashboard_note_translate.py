from google.cloud import translate_v2 as translate

def translate_text(target_language: str, text: str) -> dict:
    """Translates text into the target language.

    Args:
        target_language: The language to translate the text into (e.g., "fr" for French).
        text: The text to be translated.

    Returns:
        A dictionary containing the translated text and its detected source language.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file.
    # For more information, see:
    # https://cloud.google.com/docs/authentication/getting-started

    # Translate a note to Spanish
    note_to_translate = "This is a note about dashboard metrics."
    target_lang = "es"
    translation_result = translate_text(target_lang, note_to_translate)
    print(f"Original text: {note_to_translate}")
    print(f"Target language: {target_lang}")
    print(f"Translated text: {translation_result["translated_text"]}")
    print(f"Detected source language: {translation_result["detected_source_language"]}")

    print("\n---")

    # Translate another note to French
    note_to_translate_2 = "Performance metrics are crucial for business decisions."
    target_lang_2 = "fr"
    translation_result_2 = translate_text(target_lang_2, note_to_translate_2)
    print(f"Original text: {note_to_translate_2}")
    print(f"Target language: {target_lang_2}")
    print(f"Translated text: {translation_result_2["translated_text"]}")
    print(f"Detected source language: {translation_result_2["detected_source_language"]}")
