
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    # Google Cloud Translation API is identifiable by the client class and method names.
    # The default project associated with the environment will be used.
    response = translate_client.translate(text, target_language=target_language)

    return response["translatedText"]

if __name__ == "__main__":
    # Example usage:
    # Set up Google Cloud authentication if not already configured in your environment.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # More info: https://cloud.google.com/docs/authentication/getting-started

    note_to_translate = "Este documento contiene información importante sobre el cumplimiento y la encriptación."
    translated_note = translate_text(note_to_translate, target_language="en")
    print(f"Original: {note_to_translate}")
    print(f"Translated: {translated_note}")

    note_to_translate_french = "Ce document contient des notes de conformité importantes."
    translated_note_french = translate_text(note_to_translate_french, target_language="es")
    print(f"Original: {note_to_translate_french}")
    print(f"Translated: {translated_note_french}")
