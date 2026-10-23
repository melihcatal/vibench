from google.cloud import translate_v3 as translate


def translate_output(project_id: str, text: str, target_language_code: str):
    """Translates platform model output for another locale using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)
    return translations
