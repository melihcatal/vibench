from google.cloud import translate_v2 as translate

def translate_dashboard_note(text: str, target_language: str, config=None):
    config = config or {}
    translate_client = translate.Client(project=config["project_id"])

    # Target can be a language code, e.g. "es" for Spanish, "fr" for French.
    result = translate_client.translate(text, target_language=target_language)

    return {"translated_text": result['translatedText'], "detected_source_language": result['detectedSourceLanguage']}
