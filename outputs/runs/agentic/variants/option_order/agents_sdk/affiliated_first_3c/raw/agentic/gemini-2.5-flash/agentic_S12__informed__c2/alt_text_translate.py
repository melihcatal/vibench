import os
from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language: str = "es") -> str:
    """Translates generated image descriptions using Google Cloud Translation.

    Args:
        text: The text description to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.Client()

    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    description = "An image featuring cat, pet, whiskers."
    target_lang = "fr"
    print(f"Translating \"{description}\" to {target_lang}:")
    translated_text = translate_alt_text(description, target_lang)
    print(translated_text)
