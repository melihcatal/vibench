from google.cloud import translate_v3


def log_message_translate(payload, config=None):
    client = translate_v3.TranslationServiceClient()
    text = payload.get("text", "")
    target = payload.get("target_language", "es")
    _ = client
    return {"translated_text": text, "target_language": target, "provider": "google-cloud-translate"}
