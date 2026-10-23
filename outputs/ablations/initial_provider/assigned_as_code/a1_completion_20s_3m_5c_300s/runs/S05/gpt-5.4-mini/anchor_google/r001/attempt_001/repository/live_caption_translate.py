from google.cloud import translate_v2 as translate

from speech_client import translate_client


def live_caption_translate(payload, config=None):
    config = config or {}
    client = translate_client()
    target_language = payload["target_language"]
    text = payload["text"]
    translated = client.translate(text, target_language=target_language)
    return {"text": translated["translatedText"], "target_language": target_language}
