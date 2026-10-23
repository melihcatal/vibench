import os
from google.cloud import translate_v3 as translate

def translate_text(
    text: str,
    project_id: str,
    source_language_code: str,
    target_language_code: str,
) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        project_id: The ID of the Google Cloud project.
        source_language_code: The language code of the input text (e.g., "en-US").
        target_language_code: The language code to translate the text to (e.g., "es").

    Returns:
        The translated text.
    """

    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        text_to_translate = "This note contains important compliance information."
        source_lang = "en-US"
        target_lang = "es"

        translated_result = translate_text(
            text_to_translate, project_id, source_lang, target_lang
        )
        print(f"Original text: {text_to_translate}")
        print(f"Translated text ({target_lang}): {translated_result}")
