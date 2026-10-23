from google.cloud import translate_v3 as translate

def translate_text_with_glossary(
    text: str,
    target_language_code: str,
    project_id: str,
    glossary_id: str,
    source_language_code: str = "en",
) -> translate.TranslateTextResponse:
    """Translates a given text using a glossary.

    Args:
        text: The text to translate.
        target_language_code: The language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.
        glossary_id: The ID of the glossary to use.
        source_language_code: The language code of the source language (e.g., "en" for English).

    Returns:
        A TranslateTextResponse object containing the translated text.
    """

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    glossary_path = client.glossary_path(project_id, "global", glossary_id)

    glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary_path)

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set mime type
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "glossary_config": glossary_config,
        }
    )
    return response

def translate_text(
    text: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en",
) -> translate.TranslateTextResponse:
    """Translates a given text without using a glossary.

    Args:
        text: The text to translate.
        target_language_code: The language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.
        source_language_code: The language code of the source language (e.g., "en" for English).

    Returns:
        A TranslateTextResponse object containing the translated text.
    """

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set mime type
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )
    return response
