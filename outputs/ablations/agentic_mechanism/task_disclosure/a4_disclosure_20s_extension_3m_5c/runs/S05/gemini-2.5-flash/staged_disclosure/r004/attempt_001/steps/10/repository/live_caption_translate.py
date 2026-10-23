
from google.cloud import translate_v2 as translate

def translate_live_caption(text, target_language="es"):
    """Translates a given text into the target language using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The language to translate to (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    # Instantiates a client for Google Cloud Translation
    translate_client = translate.Client()

    # Google Cloud Translation can detect the source language automatically
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    caption = "Hello, how are you doing today?"
    translated_caption = translate_live_caption(caption, target_language="fr") # Translate to French
    print(f"Original: {caption}")
    print(f"Translated (French): {translated_caption}")

    caption_spanish = "Me gustaría una taza de café, por favor."
    translated_caption_english = translate_live_caption(caption_spanish, target_language="en") # Translate to English
    print(f"Original: {caption_spanish}")
    print(f"Translated (English): {translated_caption_english}")
