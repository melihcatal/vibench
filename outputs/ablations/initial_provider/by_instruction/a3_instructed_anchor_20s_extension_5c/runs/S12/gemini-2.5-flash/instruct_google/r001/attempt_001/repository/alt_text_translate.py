from google.cloud import translate_v3 as translate

def translate_alt_text(text: str, target_language_code: str = "en", project_id: str = None):
    """Translates generated image descriptions using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language_code: The BCP-47 language code to translate the text into (e.g., 'en' for English).
        project_id: The Google Cloud project ID. If not provided, it will be inferred from the environment.

    Returns:
        The translated text.
    """
    if not project_id:
        # Fallback to a common method to get project_id if not explicitly provided.
        # In a real application, this would likely be set via environment variables
        # or more robust configuration management.
        try:
            import google.auth
            credentials, project_id = google.auth.default()
        except Exception:
            raise ValueError("Google Cloud project ID must be provided or discoverable from the environment.")

    client = translate.TranslationServiceClient()
    location = "global"  # Or a specific region if preferred

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "target_language_code": target_language_code,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    
    return " ".join(translated_texts)
