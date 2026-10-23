import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_locale: str) -> dict:
    client = translate.Client()
    result = client.translate(text, target_language=target_locale, format_="text")
    return {"translated_text": result.get("translatedText"), "target_locale": target_locale}
