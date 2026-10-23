from google.cloud import translate_v3 as translate
import os

def multilingual_query_translate(payload, config=None):
    config = config or {}
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Replace with your GCP project ID
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    query_text = payload["query"]
    target_languages = payload["target_languages"]
    translated_queries = {}

    for lang_code in target_languages:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [query_text],
                "target_language_code": lang_code,
            }
        )
        for translation in response.translations:
            translated_queries[lang_code] = translation.translated_text

    return {"original_query": query_text, "translated_queries": translated_queries}
