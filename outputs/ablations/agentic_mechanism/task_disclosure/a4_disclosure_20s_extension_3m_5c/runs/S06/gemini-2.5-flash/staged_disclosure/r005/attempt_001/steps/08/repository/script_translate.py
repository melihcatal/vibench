
import os
from google.cloud import translate_v3 as translate

def translate_text(project_id: str, text: str, target_language: str) -> str:
    """Translates text into the target language."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or your specific region
    parent = f"projects/{project_id}/locations/{location}"

    # Wrap the text in a list for the API call
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

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id") 
    
    # Example usage
    script_to_translate = "Hello, how are you today? This is a test script for translation."
    target_lang = "es"  # Spanish

    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual GCP Project ID.")
    else:
        print(f"Original text: {script_to_translate}")
        translated_script = translate_text(project_id, script_to_translate, target_lang)
        print(f"Translated text ({target_lang}): {translated_script}")
