from google.cloud import translate_v3 as translate

from storage_models import normalize_language


def stored_text_translate(payload, config=None):
    client = translate.TranslationServiceClient()
    project_id = (config or {}).get("project_id")
    parent = f"projects/{project_id}/locations/global"
    text = payload.get("text", "")
    target_language = normalize_language(payload)
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent, mime_type="text/plain")
    translated = response.translations[0].translated_text if response.translations else ""
    return {"text": text, "translated_text": translated, "target_language": target_language}
