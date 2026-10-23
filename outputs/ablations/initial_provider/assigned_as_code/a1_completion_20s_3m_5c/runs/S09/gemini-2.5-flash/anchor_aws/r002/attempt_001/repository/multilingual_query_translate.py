from google.cloud import translate

def multilingual_query_translate(query_text, target_language, config=None):
    config = config or {}
    project_id = config.get("project_id")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided in config.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query_text],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
        
    return {"translated_queries": translations}
