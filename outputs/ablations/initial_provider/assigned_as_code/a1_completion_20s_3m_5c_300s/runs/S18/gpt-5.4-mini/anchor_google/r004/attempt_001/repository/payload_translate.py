from google.cloud import translate_v3 as translate


def payload_translate(payload, config=None):
    client = translate.TranslationServiceClient()
    text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
    return {"translated_text": text, "provider": "google-cloud-translate-v3"}
