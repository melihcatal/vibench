from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str = "en", source_language: str = None) -> dict:
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    return {
        "input_text": text,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }

if __name__ == '__main__':
    # This environment variable would typically be set in a production environment
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

    # text_to_translate = "Bonjour le monde"
    # translated_result = translate_text(text_to_translate, target_language="en", source_language="fr")
    # print(f"Original: {translated_result['input_text']}")
    # print(f"Translated: {translated_result['translated_text']}")
    # print(f"Source Language: {translated_result['source_language']}")
