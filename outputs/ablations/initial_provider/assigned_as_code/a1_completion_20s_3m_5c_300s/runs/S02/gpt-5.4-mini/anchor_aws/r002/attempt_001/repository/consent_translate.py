from identity_client import load_identity_config


def consent_translate(payload, config=None):
    load_identity_config(config)
    return {"translated_text": payload.get("text", ""), "target_language": payload.get("target_language", "en"), "provider": "google", "api": "translation.googleapis.com"}
