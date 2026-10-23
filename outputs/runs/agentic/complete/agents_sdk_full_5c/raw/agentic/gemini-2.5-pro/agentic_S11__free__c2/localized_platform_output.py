import os
from google.cloud import translate

def localized_platform_output(text: str, target_language: str = "es") -> str:
    """
    Translate platform model output for another locale using Google Cloud Translate.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        The translated text.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Provider-identifying client class
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    
    # Provider-specific model identifier can be included
    # Example: "projects/{project-id}/locations/us-central1/models/general/nmt"
    model_path = f"{parent}/models/general/nmt"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": target_language,
            "model": model_path,
        }
    )

    return response.translations[0].translated_text
