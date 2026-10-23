from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str = "es", source_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.Client()

    result = client.translate(text, target_language=target_language, source_language=source_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        text_to_translate = "The quick brown fox jumps over the lazy dog."
        translated_text = translate_text(text_to_translate, target_language="fr")
        print(f"Original text: {text_to_translate}")
        print(f"Translated to French: {translated_text}")

        text_to_translate_es = "Hello world"
        translated_text_es = translate_text(text_to_translate_es, target_language="es")
        print(f"Original text: {text_to_translate_es}")
        print(f"Translated to Spanish: {translated_text_es}")
