import os

from google.cloud import translate_v3 as translate


def multilingual_query_translate(payload, config=None):
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Please set GOOGLE_CLOUD_PROJECT environment variable or pass it directly.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    query = payload["query"]
    target_language_code = payload["target_language_code"]

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "target_language_code": target_language_code,
        }
    )

    translated_queries = [translation.translated_text for translation in response.translations]
    return {"translated_query": translated_queries[0] if translated_queries else ""}
