
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_locale: str = "es") -> str:
    """
    Translates text using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_locale: The target language locale (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_locale)
    return result["translatedText"]

if __name__ == "__main__":
    example_text = "Hello, world! This is a platform model output."
    translated_output = translate_text(example_text, "fr") # Translate to French
    print(f"Original text: {example_text}")
    print(f"Translated to French: {translated_output}")

    translated_output_spanish = translate_text(example_text, "es") # Translate to Spanish
    print(f"Translated to Spanish: {translated_output_spanish}")
