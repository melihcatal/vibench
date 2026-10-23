from google.cloud import translate_v3beta1 as translate

def translate_query(text: str, target_language: str = "en") -> str:
    """Translates a given text to the target language using Google Cloud Translation API.
    
    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en" for English).
                         Defaults to "en".
    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    # Replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID
    # For example projects/your-project-id
    project_id = "YOUR_PROJECT_ID" 
    
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text

