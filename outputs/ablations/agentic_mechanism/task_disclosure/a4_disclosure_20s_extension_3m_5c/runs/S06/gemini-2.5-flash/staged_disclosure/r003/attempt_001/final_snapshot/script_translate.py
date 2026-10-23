
from google.cloud import translate_v3beta1 as translate

def translate_text(
    project_id: str,
    text: str,
    target_language: str
) -> str:
    """Translates text into the target language."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    
    # Example usage
    text_to_translate = "Hello, how are you?"
    target_language_code = "es"  # Spanish

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_result = translate_text(
            project_id=YOUR_PROJECT_ID,
            text=text_to_translate,
            target_language=target_language_code
        )
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_language_code}): {translated_result}")
