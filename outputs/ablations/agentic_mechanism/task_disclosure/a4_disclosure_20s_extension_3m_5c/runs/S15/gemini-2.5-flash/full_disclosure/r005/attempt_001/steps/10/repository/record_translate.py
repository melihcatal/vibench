from google.cloud import translate_v3beta1
import os

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates a given text into the target language using Google Cloud Translation."""
    client = translate_v3beta1.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    if response.translations:
        return response.translations[0].translated_text
    return text

if __name__ == '__main__':
    # Example usage (replace with your actual project ID and text)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    text_to_translate = "Hello, world!"
    target_lang = "es"
    translated_text = translate_text(text_to_translate, target_lang, project_id)
    print(f"Original: {text_to_translate}")
    print(f"Translated ({target_lang}): {translated_text}")
