import os
from google.cloud import translate_v3 as translate

def translate_text_with_glossary(
    project_id: str,
    text_content: str,
    target_language: str,
    glossary_id: str,
    source_language: str = "en",
) -> translate.TranslationResponse:
    """Translates a given text into the target language using a glossary.

    Args:
        project_id: The ID of the GCP project.
        text_content: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        glossary_id: The ID of the glossary to use for translation.
        source_language: The language of the input text (defaults to "en").

    Returns:
        The translation response.
    """

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    # Set glossary configuration
    # For more information on glossaries, see https://cloud.google.com/translate/docs/advanced/glossary
    glossary_path = client.glossary_path(project_id, "global", glossary_id)
    glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary_path)

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language,
            "target_language_code": target_language,
            "glossary_config": glossary_config,
        }
    )

    return response

def translate_text(
    project_id: str,
    text_content: str,
    target_language: str,
    source_language: str = "en",
) -> translate.TranslationResponse:
    """Translates a given text into the target language.

    Args:
        project_id: The ID of the GCP project.
        text_content: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en").

    Returns:
        The translation response.
    """

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    return response

if __name__ == "__main__":
    # Example usage (replace with your actual project ID, text, and target language)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        text_to_translate = "Hello, how are you?"
        target_lang = "es"  # Spanish

        print(f"Translating '{text_to_translate}' to {target_lang} using Google Cloud Translation API...")
        translation_response = translate_text(project_id, text_to_translate, target_lang)

        if translation_response.translations:
            for translation in translation_response.translations:
                print(f"Translated text: {translation.translated_text}")
        else:
            print("No translation found.")

        # Example with glossary (uncomment and provide a valid glossary_id if you have one)
        # glossary_id = "your-glossary-id"
        # print(f"
Translating '{text_to_translate}' to {target_lang} with glossary '{glossary_id}'...")
        # glossary_translation_response = translate_text_with_glossary(project_id, text_to_translate, target_lang, glossary_id)
        # if glossary_translation_response.translations:
        #     for translation in glossary_translation_response.translations:
        #         print(f"Translated text (with glossary): {translation.translated_text}")
        # else:
        #     print("No translation found with glossary.")
