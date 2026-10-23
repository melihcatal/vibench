from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language_code: str = "es", source_language_code: str = "en") -> str:
    """Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        source_language_code: The language code of the input text (e.g., "en" for English).

    Returns:
        The translated text.
    """
    if not text.strip():
        return ""

    client = translate.Client()

    # Text can also be a sequence of strings, but for live captions, we process one at a time.
    result = client.translate(text, target_language=target_language_code, source_language=source_language_code)

    translated_text = result["translatedText"]
    # print(f"Original: '{text}' ({result['detectedSourceLanguage']}), Translated: '{translated_text}' ({target_language_code})")
    return translated_text

# Example usage (can be integrated with a live caption stream)
if __name__ == "__main__":
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or ensure gcloud is authenticated
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file for Google Cloud Translation.")
        print("Without credentials, the translation functionality will likely fail.")

    caption_chunk_en = "Hello, how are you doing today? This is a test caption."
    caption_chunk_es = translate_text(caption_chunk_en, target_language_code="es")
    print(f"English: {caption_chunk_en}")
    print(f"Spanish: {caption_chunk_es}")

    caption_chunk_fr = translate_text(caption_chunk_en, target_language_code="fr")
    print(f"French: {caption_chunk_fr}")

    caption_chunk_zh = translate_text("What is the weather like today?", target_language_code="zh-CN")
    print(f"Chinese (Simplified): {caption_chunk_zh}")
