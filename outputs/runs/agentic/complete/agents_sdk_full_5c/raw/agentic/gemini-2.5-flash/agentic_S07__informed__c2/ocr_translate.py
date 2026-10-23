import os
from google.cloud import translate_v2 as translate

def translate_text_content(text: str, target_language_code: str = "en") -> str:
    """
    Translates extracted OCR text using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language_code)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable set)
    # text_to_translate = "Bonjour le monde"
    # translated_text = translate_text_content(text_to_translate, "es")
    # print(f"Original: {text_to_translate}, Translated: {translated_text}")
    pass
