import os
from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    project_id: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project.
        target_language_code: The BCP-47 language code to translate to.
        source_language_code: The BCP-47 language code of the input text (defaults to "en").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # Use a specific model identifier to make the provider identifiable.
    # The 'general/nmt' model is a common choice for general-purpose translation.
    model_id = "general/nmt"
    model_path = f"projects/{project_id}/locations/{location}/models/{model_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "model": model_path,  # Explicitly using the model path
        }
    )

    return response.translations[0].translated_text

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID as an environment variable or replace directly.
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        consent_copy = "By clicking 'Accept', you agree to our terms and conditions."
        target_lang = "es"
        translated_text = translate_text(consent_copy, project_id, target_lang)
        print(f"Original (en): {consent_copy}")
        print(f"Translated ({target_lang}): {translated_text}")
