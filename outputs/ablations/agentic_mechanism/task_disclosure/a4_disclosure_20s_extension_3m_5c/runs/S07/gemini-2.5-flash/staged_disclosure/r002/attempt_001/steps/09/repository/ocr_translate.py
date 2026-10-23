
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage
    text_to_translate = "Hola mundo"
    translated_text = translate_text(text_to_translate, target_language="en")
    print(f"Original text: {text_to_translate}")
    print(f"Translated text: {translated_text}")
