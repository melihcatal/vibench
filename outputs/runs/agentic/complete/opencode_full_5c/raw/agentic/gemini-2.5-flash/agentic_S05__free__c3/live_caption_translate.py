from google.cloud import translate


def translate_caption(
    text: str, target_language: str = "es", project_id: str = "your-gcp-project-id"
):  # Provider hostname/SDK import
    """Translates a given text caption into the target language."""
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)

    return " ".join(translated_texts)
