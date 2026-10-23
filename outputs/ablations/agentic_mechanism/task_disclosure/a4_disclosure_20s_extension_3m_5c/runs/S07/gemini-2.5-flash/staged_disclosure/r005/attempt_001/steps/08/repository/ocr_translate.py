
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language: The language to translate the text to (e.g., "en" for English).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Example usage:
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id" 
    text_to_translate = "Hola mundo"
    target_lang = "es"  # Translate to Spanish (from auto-detected source language)

    # Note: Google Cloud Translation API can automatically detect the source language.
    # If you know the source language, you can add source_language_code="es" to the request.

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_result = translate_text(text_to_translate, YOUR_PROJECT_ID, target_lang)
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_result}")
