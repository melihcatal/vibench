import os
from google.cloud import translate_v2 as translate

def appeal_translate(text: str, target_language: str = "en") -> str:
    """Translate appeal text for review using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The language code to translate the text into (e.g., 'en' for English).

    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # default authentication is configured for Google Cloud.
    # The client will automatically pick up credentials from the environment.
    client = translate.Client()

    if not text:
        return ""

    try:
        result = client.translate(text, target_language=target_language)
        translated_text = result["translatedText"]
        # Google Cloud Translation automatically handles HTML entities if present, decode them
        return translated_text.replace('&#39;', ''''').replace('&quot;', '\"')
    except Exception as e:
        print(f"Error translating appeal text with Google Cloud Translation: {e}")
        return "Error during translation."

if __name__ == "__main__":
    # Example usage (requires Google Cloud credentials set up, e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    # original_text = "Hallo, dies ist ein Beschwerdetext auf Deutsch."
    # translated = appeal_translate(original_text, target_language="en")
    # print(f"Original: '{original_text}'")
    # print(f"Translated: '{translated}'")

    # original_text_fr = "Ceci est un texte d'appel en français."
    # translated_fr = appeal_translate(original_text_fr, target_language="es")
    # print(f"Original: '{original_text_fr}'")
    # print(f"Translated: '{translated_fr}'")
    pass
