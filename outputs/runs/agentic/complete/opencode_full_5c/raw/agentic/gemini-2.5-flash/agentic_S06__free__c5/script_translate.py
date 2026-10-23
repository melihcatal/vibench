from google.cloud import translate_v3 as translate


def translate_text(project_id: str, text: str, target_language_code: str) -> str:
    """Translates text into the target language using Google Cloud Translation.

    Args:
        project_id: The ID of the Google Cloud project.
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es").

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
            "target_language_code": target_language_code,
        }
    )

    # Display the translation for the first input. (There's only one in this case.)
    for translation in response.translations:
        return translation.translated_text
    return ""
