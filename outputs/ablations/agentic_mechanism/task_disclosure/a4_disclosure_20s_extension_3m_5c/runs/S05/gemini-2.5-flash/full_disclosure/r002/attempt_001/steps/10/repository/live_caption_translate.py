from google.cloud import translate

def translate_caption_chunk(text: str, target_language: str) -> str:
    """
    Translates a chunk of caption text into a specified target language using Google Cloud Translation.

    Args:
        text: The caption text to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    
    # Google Cloud project ID can be automatically detected or explicitly set
    # For demonstration, we assume it's set up in the environment or gcloud config
    project_id = client.project_path("[YOUR_PROJECT_ID]") # Replace with your actual project ID or ensure env var is set

    response = client.translate_text(
        parent=project_id,
        contents=[text],
        target_language_code=target_language,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
