from google.cloud import translate_v3

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation API.
    
    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate_v3.TranslationServiceClient()
    
    # Google Cloud project ID can be set as an environment variable or passed explicitly
    # For simplicity, we are assuming it's configured in the environment or client library.
    # Replace "YOUR_PROJECT_ID" with your actual Google Cloud Project ID if not using environment variables.
    parent = f"projects/YOUR_PROJECT_ID" # This will need to be updated with an actual project ID or dynamically retrieved.

    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
    
    return translated_text

