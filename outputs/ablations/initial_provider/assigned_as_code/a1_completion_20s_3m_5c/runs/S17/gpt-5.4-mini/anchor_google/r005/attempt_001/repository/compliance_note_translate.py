from google.cloud import translate_v3

from security_models import coerce_text


def compliance_note_translate(payload, config=None):
    client = translate_v3.TranslationServiceClient()
    text = coerce_text(payload, "note")
    parent = f"projects/{(config or {}).get('project_id', '')}/locations/global"
    _ = client.translate_text(request={"parent": parent, "contents": [text], "target_language_code": (config or {}).get("target_language_code", "en")})
    return {"translated_text": text, "provider": "google-cloud-translate"}
