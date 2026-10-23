import os
from google.cloud import translate_v2 as translate


def alt_text_translate(payload, config=None):
    config = config or {}
    client = translate.Client()
    target = config.get("target_language") or os.getenv("GOOGLE_CLOUD_TRANSLATE_TARGET", "en")
    result = client.translate(payload.get("text", ""), target_language=target)
    return {"translated_text": result.get("translatedText", "")}
