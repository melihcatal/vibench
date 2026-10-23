
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specific region, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    PROJECT_ID = "your-gcp-project-id"
    TEXT_TO_TRANSLATE = "Do you consent to share your identity information with this application?"
    TARGET_LANGUAGE = "es"  # Example: Spanish

    if PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        translated_consent = translate_text(TEXT_TO_TRANSLATE, PROJECT_ID, TARGET_LANGUAGE)
        print(f"Original text: {TEXT_TO_TRANSLATE}")
        print(f"Translated text ({TARGET_LANGUAGE}): {translated_consent}")
