from google.cloud import translate_v2 as translate


def alt_text_translate(payload, config=None):
    config = config or {}
    client = translate.Client()
    result = client.translate(payload["text"], target_language=config.get("target_language", "en"))
    return {"translated_text": result["translatedText"]}
