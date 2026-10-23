from google.cloud import translate_v3 as translate
import os

def translate_markup(html_content: str, target_language_code: str, source_language_code: str = None) -> str:
    """Translates HTML or markup while preserving tags."""
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/html",
    )

    if response.translations:
        return response.translations[0].translated_text
    return html_content
