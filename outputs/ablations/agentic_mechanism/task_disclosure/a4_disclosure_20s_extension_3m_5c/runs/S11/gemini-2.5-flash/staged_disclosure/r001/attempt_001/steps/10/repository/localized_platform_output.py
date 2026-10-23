from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """Translates text into the target language using Google Cloud Translation API."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "Hello, world!"
    target_language = "es"  # Spanish
    translated_text = translate_text(text_to_translate, target_language)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text ({target_language}): {translated_text}")
