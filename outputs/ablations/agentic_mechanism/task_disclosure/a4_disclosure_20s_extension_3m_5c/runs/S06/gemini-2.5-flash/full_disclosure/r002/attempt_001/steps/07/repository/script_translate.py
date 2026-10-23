from google.cloud import translate_v3 as translate

def translate_script(
    text: str,
    project_id: str,
    target_language_code: str,
    source_language_code: str = None,
) -> str:
    """Translates a given text using Google Cloud Translation."""

    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # Prepare translation request
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    # Return the translated text
    if response.translations:
        return response.translations[0].translated_text
    return ""
