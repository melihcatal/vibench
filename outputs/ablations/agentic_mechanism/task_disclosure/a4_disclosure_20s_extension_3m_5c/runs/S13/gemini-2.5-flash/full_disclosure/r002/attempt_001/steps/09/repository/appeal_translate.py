from google.cloud import translate_v3 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation.

    Args:
        text: The appeal text to translate.
        target_language: The language to translate the text into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    # Replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID
    project_id = "YOUR_PROJECT_ID"  
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code="auto",
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text
