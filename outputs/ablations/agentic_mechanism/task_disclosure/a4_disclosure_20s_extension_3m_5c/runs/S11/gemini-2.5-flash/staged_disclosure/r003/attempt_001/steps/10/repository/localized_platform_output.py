from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud project ID
    # This can be set as an environment variable or passed directly
    # For example, in your shell: export GOOGLE_CLOUD_PROJECT="your-project-id"
    project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID" 

    # Example platform model output
    platform_model_output = "The quick brown fox jumps over the lazy dog."

    # Target locale (e.g., French)
    target_locale = "fr"

    if project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud project ID.")
    else:
        localized_output = translate_text(platform_model_output, target_locale, project_id)
        print(f"Original output: {platform_model_output}")
        print(f"Localized output ({target_locale}): {localized_output}")
