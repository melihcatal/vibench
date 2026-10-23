from google.cloud import translate_v2 as translate


def welcome_translate(payload, config=None):
    config = config or {}
    client = translate.Client()
    target = payload.get("locale") or config.get("locale", "en")
    result = client.translate(payload["text"], target_language=target)
    return {"translated_text": result["translatedText"], "locale": target}
