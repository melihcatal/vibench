from google.cloud import translate_v2 as translate

from identity_client import normalize_locale


def welcome_translate(text: str, locale: str):
    client = translate.Client()
    result = client.translate(text, target_language=normalize_locale(locale))
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result.get("detectedSourceLanguage"),
    }
