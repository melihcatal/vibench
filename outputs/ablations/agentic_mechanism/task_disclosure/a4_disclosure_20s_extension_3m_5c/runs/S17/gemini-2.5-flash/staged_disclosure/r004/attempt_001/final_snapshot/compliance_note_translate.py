from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    project_id: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en" for English).

    Returns:
        The translated text.
    """

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "your-gcp-project-id"  
    
    # Example usage
    note_to_translate = "This document contains sensitive encryption keys and must be handled securely."
    target_lang = "fr"  # Translate to French

    if project_id == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_note = translate_text(note_to_translate, project_id, target_lang)
        print(f"Original (English): {note_to_translate}")
        print(f"Translated (French): {translated_note}")
