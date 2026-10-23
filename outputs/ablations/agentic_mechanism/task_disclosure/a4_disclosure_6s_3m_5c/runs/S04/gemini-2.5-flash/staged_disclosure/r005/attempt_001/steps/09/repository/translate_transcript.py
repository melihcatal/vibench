from google.cloud import translate_v3 as translate

def translate_text_with_glossary(
    project_id: str,
    text_content: str,
    target_language: str,
    glossary_id: str,
    location: str = "global",
) -> translate.TranslationServiceClient:
    """Translates a given text using a glossary.

    Args:
        project_id: The ID of the GCP project.
        text_content: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        glossary_id: The ID of the glossary to use.
        location: The location of the glossary. Default is "global".
    """

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    glossary = client.glossary_path(
        project_id, location, glossary_id
    )
    glossary_config = translate.TranslateTextGlossaryConfig(
        glossary=glossary
    )

    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        target_language_code=target_language,
        glossary_config=glossary_config,
    )

    for translation in response.translations:
        return translation.translated_text

if __name__ == "__main__":
    # Replace with your actual project ID, text, target language, and glossary ID
    project_id = "your-gcp-project-id"
    text_to_translate = "Hello, world!"
    target_lang = "es"
    your_glossary_id = "your-glossary-id"

    translated_segment = translate_text_with_glossary(
        project_id, text_to_translate, target_lang, your_glossary_id
    )
    print(f"Translated text: {translated_segment}")
