import os
from google.cloud import translate

def translate_text_google_cloud(text: str, target_language_code: str, project_id: str, source_language_code: Optional[str] = None) -> dict:
    """
    Translates platform model output for another locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = translate.TranslationServiceClient()

    location = "global"  # Or a specific region if preferred
    parent = f"projects/{project_id}/locations/{location}"

    # Wrap text in a list for the API call
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    translated_output = {
        "translated_text": response.translations[0].translated_text,
        "detected_source_language_code": response.translations[0].detected_language_code,
        "raw_response": response.translations[0].__dict__ # Expose raw SDK object details if needed
    }
    return translated_output

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and your project ID is configured.
    # https://cloud.google.com/docs/authentication/application-default-credentials
    project_id = "your-gcp-project-id"
    sample_text = "Hello, how are you?"
    target_lang = "es"

    try:
        translation_results = translate_text_google_cloud(sample_text, target_lang, project_id)
        print(f"Original Text: {sample_text}")
        print(f"Translated Text ({target_lang}): {translation_results['translated_text']}")
        print(f"Detected Source Language: {translation_results['detected_source_language_code']}")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
