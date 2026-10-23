
from google.cloud import translate_v2 as translate

def translate_text(target_language: str, text: str) -> dict:
    """Translates text into the target language using Google Cloud Translation.

    Args:
        target_language: The language to translate the text into (e.g., "en" for English, "es" for Spanish).
        text: The text to be translated.

    Returns:
        A dictionary containing the translated text and the detected source language.
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
    # Set your Google Cloud credentials using GOOGLE_APPLICATION_CREDENTIALS environment variable
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    text_to_translate = "Hola mundo, ¿cómo estás?"
    target_lang = "en"
    translated_output = translate_text(target_lang, text_to_translate)
    print(f"Original text: {text_to_translate}")
    print(f"Target language: {target_lang}")
    print(f"Translated text: {translated_output['translated_text']}")
    print(f"Detected source language: {translated_output['detected_source_language']}")

    text_to_translate_2 = "Hello, how are you?"
    target_lang_2 = "es"
    translated_output_2 = translate_text(target_lang_2, text_to_translate_2)
    print(f"
Original text: {text_to_translate_2}")
    print(f"Target language: {target_lang_2}")
    print(f"Translated text: {translated_output_2['translated_text']}")
    print(f"Detected source language: {translated_output_2['detected_source_language']}")
