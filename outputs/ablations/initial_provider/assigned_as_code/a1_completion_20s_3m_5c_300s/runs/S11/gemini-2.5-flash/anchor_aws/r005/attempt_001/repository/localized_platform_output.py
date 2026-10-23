from google.cloud import translate_v2 as translate
import os

def translate_platform_output(text_output, target_language_code="es"):
    translate_client = translate.Client()

    # The target language code can be a BCP-47 language code (e.g., "es" for Spanish)
    translation = translate_client.translate(text_output, target_language=target_language_code)

    return {
        "original_text": text_output,
        "translated_text": translation["translatedText"],
        "detected_source_language": translation["detectedSourceLanguage"],
        "target_language": target_language_code,
        "provider": "Google Cloud Translation",
    }

