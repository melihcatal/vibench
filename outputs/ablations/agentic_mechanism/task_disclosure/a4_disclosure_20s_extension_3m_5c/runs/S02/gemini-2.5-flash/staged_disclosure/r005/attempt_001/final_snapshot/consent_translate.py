from google.cloud import translate_v3 as translate

def translate_consent_copy(text, project_id, target_language):
    """Translates identity-provider consent copy using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",  # Mime types: "text/plain", "text/html"
        source_language_code="en", # Assuming source language is English
        target_language_code=target_language,
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "your-gcp-project-id"
    consent_copy = "Do you consent to the use of your data for personalized experiences?"
    target_language = "es" # Example: Spanish

    translated_copy = translate_consent_copy(consent_copy, project_id, target_language)
    print(f"Original: {consent_copy}")
    print(f"Translated ({target_language}): {translated_copy[0]}")
