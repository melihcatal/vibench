import os
from google.cloud import translate_v3 as translate

def multilingual_query_translate(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("google_cloud_project") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    if not project_id:
        raise ValueError("Google Cloud project ID not provided or found in environment variables.")

    client = translate.TranslationServiceClient()

    location = config.get("translate_location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    parent = f"projects/{project_id}/locations/{location}"

    query = payload.get("query", "")
    target_language_code = payload.get("target_language_code", "en")
    source_language_code = payload.get("source_language_code", "auto") # 'auto' for automatic detection

    if not query:
        return {"translated_query": "", "source_language_code": ""}

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code if source_language_code != "auto" else None,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return {
        "translated_query": translated_text,
        "source_language_code": detected_source_language,
        "target_language_code": target_language_code
    }
