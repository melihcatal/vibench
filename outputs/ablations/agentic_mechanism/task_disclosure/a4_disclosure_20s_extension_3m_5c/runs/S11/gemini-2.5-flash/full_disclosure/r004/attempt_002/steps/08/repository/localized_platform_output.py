from google.cloud import translate_v3 as translate

def translate_text_with_glossary(
    project_id: str,
    text: str,
    target_language_code: str,
    glossary_id: str,
    location: str = "global",
) -> str:
    """Translates a given text using a glossary.

    Args:
        project_id: Your Google Cloud project ID.
        text: The text to translate.
        target_language_code: The language code of the target language (e.g., "es" for Spanish).
        glossary_id: The ID of the glossary to use for translation.
        location: The location of the glossary. Defaults to "global".

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    glossary_path = client.glossary_path(project_id, location, glossary_id)

    glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary_path)

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "glossary_config": glossary_config,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
