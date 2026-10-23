from google.cloud import translate_v3 as translate
import os

def translate_text(text: str, project_id: str, target_language_code: str, source_language_code: str = None) -> str:
    """Translates narration scripts using Google Cloud Translation.

    Args:
        text: The text to translate.
        project_id: The Google Cloud project ID.
        target_language_code: The BCP-47 language code for the target language (e.g., "es").
        source_language_code: Optional. The BCP-47 language code for the source language (e.g., "en").
                              If not provided, the service will attempt to auto-detect.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # Handle multiple translations if necessary, but for a single input text, take the first.
    if response.translations:
        return response.translations[0].translated_text
    return text # Return original if no translation found


if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    # if project_id == "your-gcp-project-id":
    #     print("Please set GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'.")
    # else:
    #     text_to_translate = "Hello, how are you?"
    #     translated_text = translate_text(text_to_translate, project_id, "es", "en")
    #     print(f"Original: {text_to_translate}")
    #     print(f"Translated (Spanish): {translated_text}")

    # Dummy run without actual API call if project_id is not set
    text_to_translate = "Hello, how are you?"
    print(f"Original: {text_to_translate}")
    print("Translated (Spanish): [Simulated translation: Hola, ¿cómo estás?] - Actual translation requires GOOGLE_CLOUD_PROJECT")
