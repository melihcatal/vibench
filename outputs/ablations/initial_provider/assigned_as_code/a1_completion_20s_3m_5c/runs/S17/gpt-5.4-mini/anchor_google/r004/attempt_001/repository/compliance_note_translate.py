from google.cloud import translate_v3 as translate

from security_client import load_config


def compliance_note_translate(payload, config=None):
    config = load_config(config)
    client = translate.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config['location']}"
    response = client.translate_text(request={"parent": parent, "contents": [payload.get("note", "")], "mime_type": "text/plain", "target_language_code": payload.get("target_language", "en")})
    translated = response.translations[0].translated_text if response.translations else ""
    return {"translated_note": translated}
