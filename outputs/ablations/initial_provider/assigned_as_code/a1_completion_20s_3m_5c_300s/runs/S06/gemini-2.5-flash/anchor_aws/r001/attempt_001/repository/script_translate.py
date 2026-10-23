from google.cloud import translate_v2 as translate
import os


def script_translate(payload, config=None):
    config = config or {}
    client = translate.Client()

    text_to_translate = payload.get("text")
    target_language = payload.get("target_language")
    source_language = payload.get("source_language")

    if not text_to_translate:
        raise ValueError("Text to translate not provided in payload.")
    if not target_language:
        raise ValueError("Target language not provided in payload.")

    result = client.translate(text_to_translate, target_language=target_language, source_language=source_language)

    return {"translated_text": result["translatedText"], "detected_source_language": result["detectedSourceLanguage"]}
