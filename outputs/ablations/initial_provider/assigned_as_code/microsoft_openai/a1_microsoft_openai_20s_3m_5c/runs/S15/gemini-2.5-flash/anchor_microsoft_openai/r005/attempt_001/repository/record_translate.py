from google.cloud import translate_v3 as translate
import os

def translate_text(text_content, target_language_code, project_id=None, location=None, source_language_code=None):
    project_id = project_id or os.environ.get("GCP_PROJECT_ID")
    location = location or os.environ.get("GCP_LOCATION", "global") # Translation API often uses 'global'

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    # Detail on supported models: https://cloud.google.com/translate/docs/advanced/translating-text-advanced
    # For general translation, typically no specific model is needed unless for custom models.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "source_language_code": source_language_code, # Optional. If not specified, the API will attempt to detect the source language.
            "target_language_code": target_language_code,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts[0] if translated_texts else ""
