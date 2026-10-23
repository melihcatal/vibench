
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str, source_language: str = "en") -> str:
    """Translates text into the target language."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML input
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
    # Example platform model output
    platform_output = "The quick brown fox jumps over the lazy dog."
    target_locale = "es"  # Translate to Spanish

    if PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        translated_output = translate_text(platform_output, PROJECT_ID, target_locale)
        print(f"Original: {platform_output}")
        print(f"Translated ({target_locale}): {translated_output}")
