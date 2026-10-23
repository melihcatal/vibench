from google.cloud import translate_v3 as translate

def translate_caption(text: str, target_language_code: str = "es"): # Default to Spanish for example
    """Translates a given text caption into a specified target language using Google Cloud Translation API.

    Args:
        text: The text caption to translate.
        target_language_code: The BCP-47 language code of the target language.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    # The project ID needs to be configured, typically through environment variables
    # or explicit client configuration. For this example, we'll use a placeholder.
    # Replace `YOUR_PROJECT_ID` with your actual Google Cloud Project ID.
    project_id = "your-google-cloud-project-id"
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    # The Google Cloud Translation API can return multiple translations,
    # but for a single text input, we usually care about the first one.
    if response.translations:
        return response.translations[0].translated_text
    return text # Return original text if no translation found
