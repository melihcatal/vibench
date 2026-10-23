
import os
from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language: str = "es") -> str:
    """Translates generated image descriptions (alt text) to a target language."""
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']

if __name__ == '__main__':
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    original_text = "A domestic cat sleeping on a sofa."
    target_lang = "fr"
    print(f"Translating \'{original_text}\' to {target_lang}...")
    translated_text = translate_alt_text(original_text, target_lang)
    print(f"Translated text: {translated_text}")

    original_text_es = "Un gato doméstico durmiendo en un sofá."
    target_lang_en = "en"
    print(f"Translating \'{original_text_es}\' to {target_lang_en}...")
    translated_text_en = translate_alt_text(original_text_es, target_lang_en)
    print(f"Translated text: {translated_text_en}")
