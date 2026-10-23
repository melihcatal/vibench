from google.cloud import translate_v2 as translate


def record_translate(text, target_language="en"):
    client = translate.Client()
    translated = client.translate(text, target_language=target_language)
    return {"provider": "google_cloud_translate", "translated_text": translated.get("translatedText", "")}
