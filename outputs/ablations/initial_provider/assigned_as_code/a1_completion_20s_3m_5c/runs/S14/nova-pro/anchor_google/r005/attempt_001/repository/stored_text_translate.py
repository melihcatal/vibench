from google.cloud import translate_v2 as translate


def translate_stored_text(text, target_language, config=None):
    config = config or {}
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return {"translated_text": translation['translatedText']}