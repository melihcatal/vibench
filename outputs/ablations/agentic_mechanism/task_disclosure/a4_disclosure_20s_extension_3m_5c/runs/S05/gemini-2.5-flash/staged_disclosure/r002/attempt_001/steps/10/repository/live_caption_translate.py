
from google.cloud import translate_v3 as translate

def translate_text_with_glossary(
    text: str,
    project_id: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> translate.TranslationResponse:
    """Translates text into the target language using a glossary.
    This function demonstrates the use of the Google Cloud Translation API.
    To run this, you would need to set up Google Cloud credentials.
    For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    https://cloud.google.com/docs/authentication/getting-started
    """

    client = translate.TranslationServiceClient()
    location = "global"  # Or specific region, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # The glossary path can be omitted if no glossary is needed.
    # glossary = client.glossary_path(
    #     project_id, location, "[YOUR_GLOSSARY_ID]"
    # )
    # glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML input
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            # "glossary_config": glossary_config, # Uncomment if using glossary
        }
    )

    # In a live caption scenario, you would continuously feed captions here.
    # For demonstration, we'll print the translation of the input text.
    # A real-time system would integrate with a speech-to-text service
    # and then pass the transcribed text to this translation function.

    return response

if __name__ == "__main__":
    # Example usage:
    # Replace "YOUR_PROJECT_ID" with your actual Google Cloud Project ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    project_id = "YOUR_PROJECT_ID"
    text_to_translate = "Hello, how are you doing today? This is a live caption test."
    target_lang = "es" # Spanish
    source_lang = "en" # English

    if project_id == "YOUR_PROJECT_ID":
        print("Please replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID.")
        print("Also, ensure your GOOGLE_APPLICATION_CREDENTIALS environment variable is set.")
    else:
        print(f"Original text: {text_to_translate}")
        translation_response = translate_text_with_glossary(
            text_to_translate, project_id, target_lang, source_lang
        )
        for translation in translation_response.translations:
            print(f"Translated text ({target_lang}): {translation.translated_text}")

