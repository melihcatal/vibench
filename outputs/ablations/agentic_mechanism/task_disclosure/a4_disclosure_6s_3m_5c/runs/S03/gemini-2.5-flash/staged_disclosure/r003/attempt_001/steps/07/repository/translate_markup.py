from google.cloud import translate_v3

def translate_html(text: str, project_id: str, source_language: str, target_language: str) -> str:
    """Translates HTML text using Google Cloud Translation while preserving tags."""

    client = translate_v3.TranslationServiceClient()

    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        source_language_code=source_language,
        target_language_code=target_language,
        mime_type="text/html",
    )

    return response.translations[0].translated_text

