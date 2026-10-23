from google.cloud import translate_v3 as translate


def script_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.get('project_id')}/locations/{config.get('location', 'global')}"
    response = client.translate_text(contents=[payload.get("text", "")], target_language_code=config.get("target_language_code", "en"), parent=parent)
    return {"translated_text": response.translations[0].translated_text if response.translations else ""}
