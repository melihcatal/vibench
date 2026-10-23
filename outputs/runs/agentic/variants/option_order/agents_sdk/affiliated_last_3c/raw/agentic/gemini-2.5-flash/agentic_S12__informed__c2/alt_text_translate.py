import os
from google.cloud import translate

def translate_image_description(text: str, target_language: str = "es") -> str:
    """Translates a generated image description using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Assuming project ID is available
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = "global"  # Or specific region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "mime_type": "text/plain",
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT_ID are set
    sample_description = "A fluffy white cat sitting on a blue sofa."
    target_lang = "fr"

    try:
        translated_desc = translate_image_description(sample_description, target_language=target_lang)
        print(f"Original: '{sample_description}'")
        print(f"Translated to {target_lang}: '{translated_desc}'")
    except Exception as e:
        print(f"Error translating description: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT_ID environment variables are set.")
