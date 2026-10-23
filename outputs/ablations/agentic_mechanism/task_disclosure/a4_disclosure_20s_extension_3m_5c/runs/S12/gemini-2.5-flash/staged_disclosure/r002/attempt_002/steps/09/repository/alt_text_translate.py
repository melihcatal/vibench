from google.cloud import translate

def translate_alt_text(text: str, project_id: str, target_language: str, source_language: str = "en") -> str:
    """Translates text using the Google Cloud Translation API.

    Args:
        text: The text to translate.
        project_id: Your Google Cloud project ID.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The original language of the text (defaults to "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and desired text/languages)
    your_project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # <<< IMPORTANT: Replace with your actual project ID
    image_description = "A fluffy cat sitting on a keyboard."
    
    # Translate to Spanish
    spanish_translation = translate_alt_text(image_description, your_project_id, "es")
    print(f"Original: {image_description}")
    print(f"Spanish: {spanish_translation}")

    # Translate to French
    french_translation = translate_alt_text(image_description, your_project_id, "fr")
    print(f"French: {french_translation}")
