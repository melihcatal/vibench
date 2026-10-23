from google.cloud import translate_v3 as translate

def translate_platform_output(text: str, target_locale: str) -> str:
    """Translates text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    project_id = "YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID
    location = "global"  # Or your desired region
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_locale,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    platform_output = "Hello, world! This is a test."
    target_locale = "es"  # Translate to Spanish

    # Replace "YOUR_PROJECT_ID" with your actual Google Cloud Project ID
    # Ensure you have authenticated to Google Cloud (e.g., `gcloud auth application-default login`)
    # and enabled the Cloud Translation API in your project.

    try:
        translated_output = translate_platform_output(platform_output, target_locale)
        print(f"Original: {platform_output}")
        print(f"Translated ({target_locale}): {translated_output}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure 'YOUR_PROJECT_ID' is set correctly and you are authenticated to Google Cloud.")
