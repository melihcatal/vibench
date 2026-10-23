import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate to (e.g., "fr" for French).
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

    for translation in response.translations:
        return translation.translated_text
    return ""

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired target language
    # You'll need to set up authentication, e.g., by setting the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable to the path of your service account key file.
    # For more information, see:
    # https://cloud.google.com/docs/authentication/getting-started
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    onboarding_copy = "Welcome to our service! We're glad to have you."
    target_locale = "es"  # Example: Spanish

    translated_copy = translate_text(onboarding_copy, target_locale, project_id)
    print(f"Original: {onboarding_copy}")
    print(f"Translated ({target_locale}): {translated_copy}")
