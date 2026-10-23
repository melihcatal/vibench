import os
from google.cloud import translate_v3 as translate

def record_translate(text: str, target_language_code: str, project_id: str) -> str:
    """Translates user-facing document fields using Google Cloud Translation."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    
    translated_text = " ".join(translations)
    print(f"Text translated to {target_language_code} successfully.")
    return translated_text

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Replace with your actual Google Cloud Project ID
    # export GOOGLE_CLOUD_PROJECT=your-project-id
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") 
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")

    text_to_translate = "Hello, how are you?"
    target_lang = "es"
    translated = record_translate(text_to_translate, target_lang, project_id)
    print(f"Original: {text_to_translate}")
    print(f"Translated ({target_lang}): {translated}")
