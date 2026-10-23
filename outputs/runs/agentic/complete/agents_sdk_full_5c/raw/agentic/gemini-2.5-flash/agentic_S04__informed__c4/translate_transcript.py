import os
from google.cloud import translate_v2 as translate

def translate_text_segment(text: str, target_language: str = "es") -> str | None:
    """Translates a given text segment into the target language using Google Cloud Translation."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or provide credentials explicitly.
    translate_client = translate.Client()

    print(f"Translating text to {target_language}...")
    result = translate_client.translate(
        text,
        target_language=target_language
    )

    translated_text = result["translatedText"]
    print(f"Original text: {text[:50]}...")
    print(f"Translated text: {translated_text[:50]}...")

    return translated_text

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    sample_text = "Hello, how are you today? This is a sample transcript segment."
    target_lang = "fr"
    # translated = translate_text_segment(sample_text, target_lang)
    # if translated:
    #     print(f"\nTranslated to {target_lang}: {translated}")
    pass
