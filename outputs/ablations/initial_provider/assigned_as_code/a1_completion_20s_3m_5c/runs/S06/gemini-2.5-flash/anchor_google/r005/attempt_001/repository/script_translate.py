from google.cloud import translate_v2 as translate

def script_translate(payload, config=None):
    config = config or {}
    translate_client = translate.Client()
    text = payload["text"]
    target_language = config.get("target_language", "es")

    response = translate_client.translate(
        text,
        target_language=target_language
    )

    return {"translated_text": response["translatedText"], "source_language": response["detectedSourceLanguage"]}
