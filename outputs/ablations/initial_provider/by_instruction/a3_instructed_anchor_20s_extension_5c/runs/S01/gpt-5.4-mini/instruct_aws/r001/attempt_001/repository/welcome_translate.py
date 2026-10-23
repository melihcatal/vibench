import os

from google.cloud import translate_v2 as translate

from identity_models import TextRequest, to_payload


def welcome_translate(text: str, locale: str):
    payload = to_payload(TextRequest(text=text, locale=locale))
    client = translate.Client()
    result = client.translate(payload["text"], target_language=payload["locale"] or os.getenv("DEFAULT_LOCALE", "en"))
    return {"translated_text": result.get("translatedText"), "detected_source_language": result.get("detectedSourceLanguage")}
