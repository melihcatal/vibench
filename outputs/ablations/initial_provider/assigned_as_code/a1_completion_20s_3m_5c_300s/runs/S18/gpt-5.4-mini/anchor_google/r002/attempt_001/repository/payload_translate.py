from google.cloud import translate_v2 as translate


def payload_translate(payload, config=None):
    client = translate.Client()
    result = client.translate(payload["text"], target_language=payload.get("target_language", "en"))
    return {"translated_text": result["translatedText"]}
