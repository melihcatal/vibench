from google.cloud import translate_v3 as translate

def translate_text(
    text: str, project_id: str, target_language: str
) -> translate.TranslationServiceClient:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
    """

    client = translate.TranslationServiceClient()
    location = "global"  # Or your specific region if preferred
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    print(f"Translated text: {translated_text}")
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired target language
    project_id = "YOUR_PROJECT_ID"
    target_language = "es"  # Example: Spanish
    onboarding_copy = "Welcome to our service! We are happy to have you here."

    if project_id == "YOUR_PROJECT_ID":
        print("Please replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID.")
    else:
        translate_text(onboarding_copy, project_id, target_language)
